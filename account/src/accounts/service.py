
from typing import Optional
import uuid

from fastapi import HTTPException, status 

from src.accounts.schemas import ROLE_ADMIN, ROLE_USER
from src.accounts.model import  UserModel
from src.authentication.utils import hash_password
from src.accounts.dao import UserDAO
from src.accounts.schemas import UserCreate, UserCreateAdmin, UserCreateDB

from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    @classmethod
    async def create_user(
        cls,
        user_in: UserCreate | UserCreateAdmin,
        session: AsyncSession
    ) -> Optional[UserModel]:
        hashed_password = await hash_password(user_in.password)
        roles = []
        if isinstance(user_in, UserCreateAdmin):
            return await UserDAO.add(
            session=session,
            obj_in=UserCreateDB(
                **user_in.model_dump(exclude={"password"}),
                hashed_password=hashed_password,
            )
        )
        return await UserDAO.add(
            session=session,
            obj_in=UserCreateDB(
                **user_in.model_dump(exclude={"password"}),
                hashed_password=hashed_password,
                roles=roles
            )
        )
    

    @classmethod
    async def get_user(
        cls, 
        user_id: uuid.UUID, 
        session: AsyncSession
    ) -> UserModel:
        user = await UserDAO.find_one_or_none(
            session,
            UserModel.id == user_id,
        )
        if not user or not user.active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user