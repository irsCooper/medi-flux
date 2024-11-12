from typing import Optional
import uuid
from fastapi import HTTPException, status
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.dao import UserDAO
from src.accounts.model import RoleModel, UserModel
from src.accounts.schemas import ROLE_DOCTOR


class DoctorSrvice:
    @classmethod
    async def get_list_doctors(
        cls,
        nameFilter: str,
        offset: int,
        limit: int,
        session: AsyncSession,
    ) -> Optional[list[UserModel]]:
        filter = [RoleModel.name_role == ROLE_DOCTOR, UserModel.active == True]
        
        if nameFilter:
            filter.append(func.concat(UserModel.first_name, " ", UserModel.last_name).ilike(f"%{nameFilter}%"))

        doctors = await UserDAO.find_all(
            session,
            *filter,
            offset=offset,
            limit=limit
        )

        print(doctors)
        return doctors
    

    @classmethod
    async def get_doctor(
        cls,
        doctor_id: uuid.UUID,
        session: AsyncSession
    ) -> Optional[UserModel]:
        doctor = await UserDAO.find_one_or_none(
            session,
            UserModel.id == doctor_id
        )

        if doctor is None or ROLE_DOCTOR not in [role.name_role for role in doctor.roles]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )
        
        return doctor