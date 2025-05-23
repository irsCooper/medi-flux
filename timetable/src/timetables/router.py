import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.core.db_helper import db
from src.core.config import ROLE_ADMIN, ROLE_MANAGER
from src.timetables.schemas import TimetableCreate, TimetableSchema, TimetableUpdate
from src.timetables.service import TimetableService
from src.rabbit_mq.account import AccountRabbitHelper

router = APIRouter(
    prefix='/Timetable',
    tags=['Timetable']
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TimetableSchema)
async def create_timetable(
    create_timetable: TimetableCreate,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):
    await AccountRabbitHelper.get_current_role([ROLE_ADMIN, ROLE_MANAGER], valid_token)
    
    return await TimetableService.create_timetable(
        data=create_timetable,
        session=session
    )


@router.put("/{id}", response_model=TimetableSchema)
async def update_timetable(
    update_timetable: TimetableUpdate,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):
    await AccountRabbitHelper.get_current_role([ROLE_ADMIN, ROLE_MANAGER], valid_token)
    
    return await TimetableService.update_timetable(
        timetable_id=update_timetable.id,
        data=update_timetable,
        session=session
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_timetable(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):
    await AccountRabbitHelper.get_current_role([ROLE_ADMIN, ROLE_MANAGER], valid_token)
    
    await TimetableService.delete_timetable(
      timetable_id=id,
      session=session  
    )


@router.delete("/Doctor/{id}", status_code=status.HTTP_200_OK)
async def delete_timetables_for_doctor(
    doctor_id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):
    await AccountRabbitHelper.get_current_role([ROLE_ADMIN, ROLE_MANAGER], valid_token)
   
    await TimetableService.delete_timetables_for_doctor_id(
        doctor_id=doctor_id,
        session=session
    )


@router.delete("/Hospital/{id}", status_code=status.HTTP_200_OK)
async def delete_timetable_for_hoospital(
    hospital_id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):
    await AccountRabbitHelper.get_current_role([ROLE_ADMIN, ROLE_MANAGER], valid_token)

    await TimetableService.delete_timetables_for_hospital_id(
        hospital_id=hospital_id,
        session=session
    )


@router.get("/Hospital/{id}", response_model=list[TimetableSchema])
async def get_timetables_for_hospital(
    id: uuid.UUID,
    from_datetime: datetime = Query(..., alias="from"),
    to: datetime = Query(...),
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):
    return await TimetableService.get_timetables_for_hospital_id(
        hospital_id=id,
        session=session,
        from_column=from_datetime,
        to=to
    )


@router.get("/Doctor/{id}", response_model=list[TimetableSchema])
async def get_timetables_for_doctor(
    id: uuid.UUID,
    from_datetime: datetime = Query(..., alias="from"),
    to: datetime = Query(...),
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):
    return await TimetableService.get_timetables_for_doctor_id(
        doctor_id=id,
        session=session,
        from_column=from_datetime,
        to=to
    )


@router.get("/Hospital/{id}/Room/{room}", response_model=list[TimetableSchema])
async def get_timetables_for_doctor(
    id: uuid.UUID,
    room: str,
    from_datetime: datetime = Query(..., alias="from"),
    to: datetime = Query(...),
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):
    await AccountRabbitHelper.get_current_role([ROLE_ADMIN, ROLE_MANAGER], valid_token)
    
    return await TimetableService.get_timetables_for_hospital_room(
        hospital_id=id,
        room=room,
        from_column=from_datetime,
        to=to,
        session=session
    )


@router.get("/{id}/Appointments")
async def get_free_appointsment_by_timetable_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):
    return await TimetableService.get_free_appointsment_by_timetable_id(id, session)


@router.post("/{id}/Appointments")
async def create_appointsment_by_timetable_id(
    id: uuid.UUID,
    time: datetime,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: str = Depends(AccountRabbitHelper.validate_token)
):
    return await TimetableService.create_appointsment_by_timetable_id(
        timetable_id=id,
        user_id=uuid.uuid4(),
        time=time,
        session=session
    )