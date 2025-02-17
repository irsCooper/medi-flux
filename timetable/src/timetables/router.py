import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.core.db_helper import db
from src.timetables.schemas import TimetableCreate, TimetableSchema, TimetableUpdate
from src.timetables.service import TimetableService

router = APIRouter(
    prefix='/Timetable',
    tags=['Timetable']
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TimetableSchema)
async def create_timetable(
    create_timetable: TimetableCreate,
    session: AsyncSession = Depends(db.session_dependency)
):
    return await TimetableService.create_timetable(
        data=create_timetable,
        session=session
    )


@router.put("/{id}", response_model=TimetableSchema)
async def update_timetable(
    update_timetable: TimetableUpdate,
    session: AsyncSession = Depends(db.session_dependency)
):
    return await TimetableService.update_timetable(
        timetable_id=update_timetable.id,
        data=update_timetable,
        session=session
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_timetable(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency)
):
    await TimetableService.deelete_timetable(
      timetable_id=id,
      session=session  
    )


@router.delete("/Doctor/{id}", status_code=status.HTTP_200_OK)
async def delete_timetables_for_doctor(
    doctor_id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency)
):
    pass


@router.delete("/Hospital/{id}", status_code=status.HTTP_200_OK)
async def delete_timetable_for_hoospital(
    hospital_id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency)
):
    pass


@router.get("/Hospital/{id}", response_model=list[TimetableSchema])
async def get_timetables_for_hospital(
    id: uuid.UUID,
    from_datetime: datetime = Query(..., alias="from"),
    to: datetime = Query(...),
    session: AsyncSession = Depends(db.session_dependency)
):
    pass


@router.get("/Doctor/{id}", response_model=list[TimetableSchema])
async def get_timetables_for_doctor(
    id: uuid.UUID,
    from_datetime: datetime = Query(..., alias="from"),
    to: datetime = Query(...),
    session: AsyncSession = Depends(db.session_dependency)
):
    pass


@router.get("/Hospital/{id}/Room/{room}", response_model=list[TimetableSchema])
async def get_timetables_for_doctor(
    id: uuid.UUID,
    room: str,
    from_datetime: datetime = Query(..., alias="from"),
    to: datetime = Query(...),
    session: AsyncSession = Depends(db.session_dependency)
):
    pass