from datetime import datetime, timedelta
import uuid
import bcrypt
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
import jwt

from src.core.config import settings


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Authentication/SignIn")


async def hash_password(password: str) -> bytes: 
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


async def validate_password(
        password: str,
        hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )


async def encode_jwt(
        payload: dict,
        keys: str = settings.auth_jwt.private_key_path.read_text(),
        algorithms: str = settings.auth_jwt.algorithms,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    
    to_encode.update(
        exp=now + timedelta(minutes=expire_minutes),
        iat=now,
        jti=str(uuid.uuid4())
    )

    encoded = jwt.encode(
        payload=to_encode,
        key=keys,
        algorithm=algorithms
    )
    return encoded


async def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithms: str = settings.auth_jwt.algorithms
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=algorithms
    )
    return decoded