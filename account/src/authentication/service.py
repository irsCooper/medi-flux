from datetime import datetime, timedelta
from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.model import RefreshModel
from src.authentication.dao import RefreshTokenDAO
from src.accounts.dao import UserDAO
from src.accounts.model import UserModel
from src.accounts.service import UserService
from src.authentication.schemas import RefreshCreate, TokenInfo
from src.authentication.utils import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, decode_jwt, validate_password
from src.dependencies import create_token_of_type, get_current_auth_user_of_type_token, validate_token_type
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
                expire_in=int((datetime.utcnow() + timedelta(days=settings.auth_jwt.refresh_token_expire_days)).timestamp()),
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

        if user and user.active and await validate_password(password, user.hashed_password):
            return await cls.create_token(user, session)
        
        raise InvalidCredentialsException
    

    @classmethod
    async def sing_out(
        cls,
        user_id: uuid.UUID,
        session: AsyncSession
    ):
        await RefreshTokenDAO.delete(
            session, 
            RefreshModel.user_id == user_id
        )


    @classmethod
    async def validate_access_token(cls, access_token: str):
        try: 
            return await decode_jwt(access_token)
        except Exception as e:
            print(e)
            return None
        
    
    @classmethod
    async def refresh_tokens(
        cls,
        refresh_token: str,
        session: AsyncSession
    ):
        user = await get_current_auth_user_of_type_token(
            token=refresh_token, 
            token_type=REFRESH_TOKEN_TYPE, 
            session=session
        )

        return await cls.create_token(
            user=user,
            session=session
        )

    
