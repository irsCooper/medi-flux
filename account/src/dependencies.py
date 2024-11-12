from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
import jwt

from account.src.accounts.model import UserModel
from src.authentication.utils import ACCESS_TOKEN_TYPE, TOKEN_TYPE_FIELD, decode_jwt, encode_jwt
from src.core.config import settings


http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Authentication/SignIn")


async def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int 
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return await encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes
    )


async def create_token_of_type(
    token_type: str, 
    user: UserModel
) -> str:
    
    jwt_payload = {
        "sub": user.id
    }

    expire_minutes: int = settings.auth_jwt.refresh_token_expire_days * 60 * 24


    if token_type == ACCESS_TOKEN_TYPE:
        jwt_payload.update({
            "user_name": user.user_name,
            "active": user.active
        })
        expire_minutes = settings.auth_jwt.access_token_expire_minutes 
    

    return await create_jwt(
        token_type=token_type,
        token_data=jwt_payload,
        expire_minutes=expire_minutes
    )


async def validate_token_type(
    payload: dict, 
    token_type: str
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True 
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}"
    )


async def get_current_token_payload(token: str):
    try:
        payload = await decode_jwt(token)
    except jwt.InvalidTokenError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error"
        )
    return payload  