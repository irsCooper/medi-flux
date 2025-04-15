import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode

from src.rabbit_mq.base import ROUTING_KEY_CHECK_DOCTOR, ROUTING_KEY_CHECK_TOKEN
from src.rabbit_mq.client import rabbit_mq_client
from src.core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://0.0.0.0:8081/Authentication/SignIn')


class AccountRabbitHelper:
    @classmethod
    async def validate_token(cls, token: str = Depends(oauth2_scheme)):
        correlation_id = str(uuid.uuid4())

        await rabbit_mq_client.connect()
        channel = await rabbit_mq_client.create_channel()
        callback_queue = await rabbit_mq_client.create_queue(channel)

        response: bool = await rabbit_mq_client.call_and_wait_for_response(
            channel=channel,
            body=token,
            routing_key=ROUTING_KEY_CHECK_TOKEN,
            callback_queue=callback_queue,
            correlation_id=correlation_id
        )

        if response is True:
            return token
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response
        )
    

    @classmethod
    async def decoded_token(
        cls, 
        token: str,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithms: str = settings.auth_jwt.algorithms
    ) -> dict:
        return decode(
            jwt=token,
            key=public_key,
            algorithms=algorithms
        )
    
    @classmethod
    async def get_current_role(
        cls,
        roles: list,
        token: str
    ):
        decoded: dict = cls.validate_token(token)

        if any(role in roles for role in decoded.get('roles', [])):
            return
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    

    @classmethod
    async def check_doctor(cls, doctor_id: uuid.UUID):
        correlation_id = str(uuid.uuid4())

        await rabbit_mq_client.connect()
        channel = await rabbit_mq_client.create_channel()
        callback_queue = await rabbit_mq_client.create_queue(channel)

        response: bool = await rabbit_mq_client.call_and_wait_for_response(
            channel=channel,
            body=str(doctor_id),
            routing_key=ROUTING_KEY_CHECK_DOCTOR,
            callback_queue=callback_queue,
            correlation_id=correlation_id
        )

        if response is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=response
            )