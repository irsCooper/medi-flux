import uuid
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from src.rabbit_mq.client import rabbit_mq_client
from src.rabbit_mq.base import ROUTING_KEY_CHECK_TOKEN

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://192.168.0.32:8081/Authentication/SignIn')

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
    
    if response is True:
        return token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response
        )