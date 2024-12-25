from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.dao import RefreshTokenDAO
from src.accounts.dao import UserDAO
from src.accounts.model import UserModel
from src.accounts.service import UserService
from src.authentication.schemas import RefreshCreate, TokenInfo
from src.authentication.utils import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, validate_password
from src.dependencies import create_token_of_type
from src.exceptions.AuthExceptions import InvalidCredentialsException
from src.accounts.schemas import UserCreate
from src.core.config import settings


class AuthService:
    @classmethod
    async def create_token(cls, user: UserModel, session: AsyncSession) -> TokenInfo:
        access_token = await create_token_of_type(ACCESS_TOKEN_TYPE, user)

        refresh_id = uuid.uuid4()
        refresh_token = await create_token_of_type(REFRESH_TOKEN_TYPE, user, refresh_id)
        
        await RefreshTokenDAO.add(
            session,
            RefreshCreate(
                user_id=user.id,
                reftesh_token_id=refresh_id,
                reftesh_token=refresh_token,
                access_token=access_token,
                expire_in=int(datetime.utcnow().timestamp() + settings.auth_jwt.refresh_token_expire_days * 120 * 24),
            )
        )
        
        await session.commit()

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token
        )

    
    @classmethod
    async def sign_up(
        cls, 
        user_in: UserCreate, 
        session: AsyncSession
    ): 
        user = await UserService.create_user(user_in=user_in, session=session)
        return await cls.create_token(user, session)



    @classmethod
    async def sign_in(
        cls,
        username: str,
        password: str,
        session: AsyncSession,
    ):
        user: Optional[UserModel]  = await UserDAO.find_one_or_none(
            session,
            user_name=username
        )

        print(user)

        if user and user.active and await validate_password(password, user.hashed_password):
            return await cls.create_token(user, session)
        
        raise InvalidCredentialsException
    



    
