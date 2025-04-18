from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from src.rabbit_mq.client import rabbit_mq_client
from src.rabbit_mq.base import ROUTING_KEY_CHECK_TOKEN
from src.core.config import settings

import uuid
from jwt import decode

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://localhost:8081/Authentication/SignIn')

async def validate_token(token: str = Depends(oauth2_scheme)):
    correlation_id = str(uuid.uuid4())

    await rabbit_mq_client.connect()
    channel = await rabbit_mq_client.create_channel()
    callback_queue = await rabbit_mq_client.create_queue(channel)

    response: bool | str = await rabbit_mq_client.call_and_wait_for_response(
        channel=channel,
        body=token, 
        routing_key=ROUTING_KEY_CHECK_TOKEN,
        correlation_id=correlation_id,
        callback_queue=callback_queue
    )

    print(response)
    
    if response is True:
        return token
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=response
    )
    

async def get_current_role(
    roles: list, 
    token,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithms: str = settings.auth_jwt.algorithms
):
    decoded: dict = decode(
        jwt=token,
        key=public_key,
        algorithms=algorithms
    )

    if any(role in roles for role in decoded.get('roles', [])):
        return
            
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enouugh pivileges"
    )