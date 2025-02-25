from datetime import datetime, timedelta
from typing import Optional
import uuid
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.timetables.schemas import TimetableCreate, TimetableUpdate
from src.timetables.model import TimetableModel
from src.timetables.dao import TimetableDAO
from src.exception.TimetableException import TimetableNotFound, DatatimeOnFormError
from src.rabbit_mq.hospital import HospitalRabbitHelper

class TimetableService:
    @classmethod
    async def create_timetable(
        cls,
        data: TimetableCreate,
        session: AsyncSession
    ) -> Optional[TimetableModel]:
        
        await HospitalRabbitHelper.check_hospital(data.hospital_id)
        # if data.from_column >= data.to:
        #     raise DatatimeOnFormError
            
        # if data.from_column.minute != 30 and data.from_column.minute != 0:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="The minutes of the 'form' field must be a multiple of 30 or equal to 00"
        #     )
        
        # if data.from_column.second != 0:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="The secjond of the 'form' field must be a multiple of o 0"
        #     )
        
        # if data.to.minute != 30 and data.to.minute != 0:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="The minutes of the 'to' field must be a multiple of 30 or equal to 0"
        #     )
        
        # if data.to.second != 0:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="The secjond of the 'to' field must be a multiple of o 0"
        #     )
        
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
        if data.from_column >= data.to:
            raise DatatimeOnFormError
        
        timetable = await TimetableDAO.update(
            session,
            TimetableModel.id == timetable_id,
            obj_in=TimetableUpdate(**data.model_dump())
        )

        if not timetable:
            raise TimetableNotFound
        
        if timetable.appointments:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Timetable already has appointments'
            )
        
        return timetable
    

    @classmethod
    async def delete_timetable(
        cls,
        timetable_id: uuid.UUID,
        session: AsyncSession
    ):
        await TimetableDAO.delete(
            session,
            TimetableModel.id == timetable_id,
        )


    @classmethod
    async def delete_timetables_for_doctor_id(
        cls,
        doctor_id: uuid.UUID,
        session: AsyncSession
    ):
        await TimetableDAO.delete(
            session,
            TimetableModel.doctor_id == doctor_id
        )

    
    @classmethod
    async def delete_timetables_for_hospital_id(
        cls,
        hospital_id: uuid.UUID,
        session: AsyncSession
    ):
        await TimetableDAO.delete(
            session,
            TimetableModel.hospital_id == hospital_id
        )

    @classmethod
    async def get_timetables_for_doctor_id(
        cls,
        doctor_id: uuid.UUID,
        session: AsyncSession,
        from_column: datetime,
        to: datetime
    ) -> Optional[list[TimetableModel]]:
        if from_column >= to:
            raise DatatimeOnFormError
        
        return await TimetableDAO.find_all(
            session,
            and_(
                TimetableModel.doctor_id == doctor_id,
                TimetableModel.from_column < to,
                TimetableModel.to > from_column
            ),
        )
    

    @classmethod
    async def get_timetables_for_hospital_id(
        cls,
        hospital_id: uuid.UUID,
        session: AsyncSession,
        from_column: datetime,
        to: datetime
    ) -> Optional[list[TimetableModel]]:
        if from_column >= to:
            raise DatatimeOnFormError
        
        return await TimetableDAO.find_all(
            session,
            and_(
                TimetableModel.hospital_id == hospital_id,
                TimetableModel.from_column < to,
                TimetableModel.to > from_column
            ),
        )
    

    @classmethod
    async def get_timetables_for_hospital_room(
        cls,
        hospital_id: uuid.UUID,
        room: str,
        session: AsyncSession,
        from_column: datetime,
        to: datetime
    ) -> Optional[list[TimetableModel]]:
        if from_column >= to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The "to" field should be larger than the "from" field'
            )
        return await TimetableDAO.find_all(
            session,
            and_(
                TimetableModel.hospital_id == hospital_id,
                TimetableModel.room == room,
                TimetableModel.from_column < to,
                TimetableModel.to > from_column
            ),
        )