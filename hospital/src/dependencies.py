from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from src.rabbit_mq.client import rabbit_mq_client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://localhost:8081/api/Authentication/SignIn')

async def validate_token(token: str = Depends(oauth2_scheme)):
    response: bool | str = await rabbit_mq_client.call(token)
    if response is True:
        return token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response
        )