from operator import and_
from typing import Optional
import uuid
from fastapi import HTTPException, status
from fastapi.background import P
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import ROLE_DOCTOR
from src.core.db_helper import es
from src.rabbit_mq.hospital import HospitalRabbitHelper
from src.rabbit_mq.account import AccountRabbitHelper
from src.history.dao import HistoryDAO
from src.history.model import HistoryModel
from src.history.schemas import HistoryCreate, HistoryUpdate

class HistoryService: 
    @staticmethod
    async def add_history_on_es(history: HistoryModel):
        history_dict: dict = {key: value for key, value in history.__dict__.items() if not key.startswith('_sa')}
        await es.index(
            index="history",
            id=history.id,
            body=history_dict
        )


    @classmethod
    async def create_history(
        cls,
        history_create: HistoryCreate,
        session: AsyncSession
    ) -> Optional[HistoryModel]:
        
        await HospitalRabbitHelper.check_hospital_room(
            hospital_id=history_create.hospital_id,
            room=history_create.room
        )
        
        await AccountRabbitHelper.check_pacient(history_create.pacient_id)
        await AccountRabbitHelper.check_doctor(history_create.doctor_id)

        history: HistoryModel = await HistoryDAO.add(
            session=session,
            obj_in=history_create
        )

        await cls.add_history_on_es(history)
        return history

    
    @classmethod
    async def update_history(
        cls, 
        history_update: HistoryUpdate,
        session: AsyncSession
    ) -> Optional[HistoryModel]:
        
        await HospitalRabbitHelper.check_hospital_room(
            hospital_id=history_update.hospital_id,
            room=history_update.room
        )
        
        await AccountRabbitHelper.check_pacient(history_update.pacient_id)
        await AccountRabbitHelper.check_doctor(history_update.doctor_id)

        history: HistoryModel = await HistoryDAO.update(
            session,
            HistoryModel.id == history_update.id,
            obj_in=history_update
        )

        if not history: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="History not found"
            )
        
        await cls.add_history_on_es(history)

        return history
    
    
    @classmethod
    async def get_history_of_visits_and_appointments_by_account(
        cls,
        account_id: uuid.UUID,
        token: str,
        session: AsyncSession
    ):
        try:
            await AccountRabbitHelper.get_current_role(
                roles=[ROLE_DOCTOR], 
                token=token,
            )
        except:
            decoded: dict = await AccountRabbitHelper.decoded_token(token)

            if str(account_id) != decoded.get('sub'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough privileges"
                )
        
        historys = await es.search(
            index="history",
            body={
                'query': {
                    'term': {
                        'pacientId': account_id
                    }
                }
            }
        )

        res = [item['_source'] for item in historys['hits']['hits']]
        if not res:
            await AccountRabbitHelper.check_pacient(account_id)

        return res


    @classmethod
    async def get_history_of_visits_and_appointments(
        cls,
        history_id: uuid.UUID,
        token: str,
        session: AsyncSession
    ):
        res = await es.get(
            index="history", id=history_id
        )

        history = res['_source']

        if history:
            try:
                await AccountRabbitHelper.get_current_role(
                    roles=[ROLE_DOCTOR], 
                    token=token,
                )
            except:
                decoded: dict = await AccountRabbitHelper.decoded_token(token)

                if str(history["pacient_id"]) != decoded.get('sub'):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not enough privileges"
                    )
        return history
