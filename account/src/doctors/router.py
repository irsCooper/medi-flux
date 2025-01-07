from typing import Optional
import uuid
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.model import UserModel
from src.dependencies import get_current_auth_access, http_bearer
from src.doctors.service import DoctorSrvice
from src.accounts.schemas import UserView
from src.core.db_helper import db


router = APIRouter(
    prefix="/Doctors",
    tags=["Doctors"],
    dependencies=[Depends(http_bearer)]
)

# только для авторизированных!! добавить
@router.get("/", response_model=list[UserView])
async def get_list_doctors(
    offset: int,
    count: int,
    nameFilter: Optional[str] = None,
    user: UserModel = Depends(get_current_auth_access),
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
    user: UserModel = Depends(get_current_auth_access),
    session: AsyncSession = Depends(db.session_dependency)
):
    return await DoctorSrvice.get_doctor(doctor_id=id, session=session)