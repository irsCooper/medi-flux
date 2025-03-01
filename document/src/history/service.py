from operator import and_
from typing import Optional
import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import ROLE_ADMIN, ROLE_DOCTOR
from src.rabbit_mq.hospital import HospitalRabbitHelper
from src.rabbit_mq.account import AccountRabbitHelper
from src.history.dao import HistoryDAO
from src.history.model import HistoryModel
from src.history.schemas import HistoryCreate, HistoryUpdate

class HistoryService: 
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

        return await HistoryDAO.add(
            session=session,
            obj_in=history_create
        )
    
    
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

        return await HistoryDAO.update(
            session,
            HistoryModel.id == history_update.id,
            obj_in=history_update
        )
    
    
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
        
        await AccountRabbitHelper.check_pacient(account_id)

        return await HistoryDAO.find_all(
            session,
            HistoryModel.pacient_id == account_id,
        )


    @classmethod
    async def get_history_of_visits_and_appointments(
        cls,
        history_id: uuid.UUID,
        token: str,
        session: AsyncSession
    ):
        history: HistoryModel = await HistoryDAO.find_one_or_none(
            session,
            HistoryModel.id == history_id,
        )

        if history:
            try:
                await AccountRabbitHelper.get_current_role(
                    roles=[ROLE_DOCTOR], 
                    token=token,
                )
            except:
                decoded: dict = await AccountRabbitHelper.decoded_token(token)

                if str(history.pacient_id) != decoded.get('sub'):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not enough privileges"
                    )
        return history
