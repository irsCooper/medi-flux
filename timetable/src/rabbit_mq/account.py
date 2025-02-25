import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode

from src.rabbit_mq.base import ROUTING_KEY_CHECK_TOKEN
from src.rabbit_mq.client import rabbit_mq_client
from src.core.config import settings


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://192.168.0.32:8081/Authentication/SignIn')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://0.0.0.0:8081/Authentication/SignIn')


class AccountRabbitHelper:
    @classmethod
    async def validate_token(self, token: str = Depends(oauth2_scheme)):
        correlation_id = str(uuid.uuid4())

        await rabbit_mq_client.connect()
        channel = await rabbit_mq_client.create_channel()
        callback_queue = await rabbit_mq_client.create_queue(channel)

        response: bool = await rabbit_mq_client.call_and_wait_for_response(
            channel=channel,
            body=token,
            routing_key=correlation_id,
            callback_queue=callback_queue
        )

        if response is True:
            return token
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response
        )
    
    @classmethod
    async def get_current_role(
        self,
        roles: list,
        token: str,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithms: str = settings.auth_jwt.algorithms
    ):
        decoded: dict = decode(
            jwt=token,
            key=public_key,
            algorithms=algorithms
        )

        current_roles = decoded.get('roles')

        for i in range(len(current_roles)):
            for j in range(len(roles)):
                if current_roles[i] == roles[j]:
                    return
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )