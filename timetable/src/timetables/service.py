from datetime import datetime, timedelta
from typing import Optional
import uuid
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.appointments.dao import AppointmentModel, AppointmentDAO, AppointmentCreate
from src.timetables.schemas import TimetableCreate, TimetableUpdate
from src.timetables.model import TimetableModel
from src.timetables.dao import TimetableDAO
from src.exception.TimetableException import TimetableNotFound, DatatimeOnFormError
from src.rabbit_mq.hospital import HospitalRabbitHelper
from src.rabbit_mq.account import AccountRabbitHelper

class TimetableService:
    @classmethod
    async def validate_time(cls, time_value: datetime, field_name: str, to: datetime = None):
        if to:
            if time_value >= to:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="The 'from_column' must be less than 'to'"
                )

        if time_value.minute not in {0, 30}:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"The minutes of the '{field_name}' field must be 0 or 30"
            )
        
        if time_value.second != 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"The seconds of the '{field_name}' field must be 0"
            )



    @classmethod
    async def create_timetable(
        cls,
        data: TimetableCreate,
        session: AsyncSession
    ) -> Optional[TimetableModel]:
        await cls.validate_time(data.from_column, 'from', data.to)
        await cls.validate_time(data.to, 'to')
        
        await HospitalRabbitHelper.check_hospital(data.hospital_id)
        await AccountRabbitHelper.check_doctor(data.doctor_id)
        
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
        await cls.validate_time(data.from_column, 'from', data.to)
        await cls.validate_time(data.to, 'to')
        
        await HospitalRabbitHelper.check_hospital(data.hospital_id)
        await AccountRabbitHelper.check_doctor(data.doctor_id)
        
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
        await AccountRabbitHelper.check_doctor(doctor_id)

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
        await HospitalRabbitHelper.check_hospital(hospital_id)

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
        await cls.validate_time(from_column, 'from', to)
        await cls.validate_time(to, 'to')
        
        await AccountRabbitHelper.check_doctor(doctor_id)
        
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
        await cls.validate_time(from_column, 'from', to)
        await cls.validate_time(to, 'to')

        await HospitalRabbitHelper.check_hospital(hospital_id)
        
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
        await cls.validate_time(from_column, 'from', to)
        await cls.validate_time(to, 'to')
        
        await HospitalRabbitHelper.check_hospital_room(hospital_id, room)

        return await TimetableDAO.find_all(
            session,
            and_(
                TimetableModel.hospital_id == hospital_id,
                TimetableModel.room == room,
                TimetableModel.from_column < to,
                TimetableModel.to > from_column
            ),
        )
    

    @classmethod
    async def get_free_appointsment_by_timetable_id(
        cls,
        timetable_id: uuid.UUID,
        session: AsyncSession
    ):
        timetable: TimetableModel = await TimetableDAO.find_one_or_none(
            session,
            TimetableModel.id == timetable_id
        )

        if not timetable:
            raise TimetableNotFound
        
        available_slots = []
        current_time = timetable.from_column

        while current_time < timetable.to:
            available_slots.append(current_time)
            current_time += timedelta(minutes=30)

        occupied_slots_set = set(slot.time for slot in timetable.appointments)

        free_slots = [slot for slot in available_slots if slot not in occupied_slots_set]

        return {"available_slots": free_slots}
    

    @classmethod
    async def create_appointsment_by_timetable_id(
        cls,
        timetable_id: uuid.UUID,
        user_id: uuid.UUID,
        time: datetime,
        session: AsyncSession
    ):
        timetable: TimetableModel = await TimetableDAO.find_one_or_none(
            session, TimetableModel.id == timetable_id
        )

        if not timetable: 
            raise TimetableNotFound
        
        await cls.validate_time(time, 'time')
        
        if timetable.appointments:
            occupied_slots_set = set(slot.time for slot in timetable.appointments)
            if time in occupied_slots_set:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f'appointment for this time {time} already exists'
                )

        return await AppointmentDAO.add(
            session=session, 
            obj_in=AppointmentCreate(
                timetable_id=timetable_id,
                user_id=user_id,
                time=time
            )
        )