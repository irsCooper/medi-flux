from typing import Optional
import uuid
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

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
        return HistoryDAO.update(
            session,
            HistoryModel.id == history_update.id,
            obj_in=history_update
        )
    
    
    @classmethod
    async def get_history_of_visits_and_appointments_by_account(
        cls,
        account_id: uuid.UUID,
        session: AsyncSession
    ):
        return HistoryDAO.find_all(
            session,
            HistoryModel.pacient_id == account_id,
        )


    @classmethod
    async def get_history_of_visits_and_appointments(
        cls,
        history_id: uuid.UUID,
        session: AsyncSession
    ):
        return HistoryDAO.find_one_or_none(
            session,
            HistoryModel.id == history_id,
        )