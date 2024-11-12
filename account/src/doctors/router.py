from typing import Optional
import uuid
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.doctors.service import DoctorSrvice
from src.accounts.service import UserService
from src.accounts.schemas import UserCreateAdmin, UserDB, UserUpdate, UserView
from src.core.db_helper import db


router = APIRouter(
    prefix="/Doctors",
    tags=["Doctors"],
)

# только для авторизированных!! добавить
@router.get("/", response_model=list[UserView])
async def get_list_doctors(
    offset: int,
    count: int,
    nameFilter: Optional[str] = None,
    session: AsyncSession = Depends(db.session_dependency)
):
    return await DoctorSrvice.get_list_doctors(
        nameFilter=nameFilter,
        offset=offset,
        limit=count,
        session=session
    )


@router.get("/{id}", response_model=UserView)
async def get_doctor_info(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency)
):
    return await DoctorSrvice.get_doctor(doctor_id=id, session=session)