from typing import Optional
import uuid
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.timetables.schemas import TimetableCreate, TimetableUpdate
from src.timetables.model import TimetableModel
from src.timetables.dao import TimetableDAO
from src.exception.TimetableException import TimetableNotFound

class TimetableService:
    @classmethod
    async def create_timetable(
        cls,
        data: TimetableCreate,
        session: AsyncSession
    ) -> Optional[TimetableModel]:
        return await TimetableDAO.add(
            session=session,
            obj_in=TimetableCreate(**data.model_dump())
        )
    

    @classmethod
    async def update_timetable(
        cls,
        timetable_id: uuid.UUID,
        data: TimetableUpdate,
        session: AsyncSession
    ) -> Optional[TimetableModel]:
        timetable = await TimetableDAO.update(
            session,
            TimetableModel.id == timetable_id,
            obj_in=TimetableUpdate(data.model_dump())
        )

        if not timetable:
            raise TimetableNotFound
        
        return timetable
    

    @classmethod
    async def deelete_timetable(
        timetable_id: uuid.UUID,
        session: AsyncSession
    ):
        await TimetableDAO.delete(
            session,
            TimetableModel.id == timetable_id,
        )