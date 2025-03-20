import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode

from src.rabbit_mq.base import ROUTING_KEY_CHECK_DOCTOR, ROUTING_KEY_CHECK_PACIENT, ROUTING_KEY_CHECK_TOKEN
from src.rabbit_mq.client import rabbit_mq_client
from src.core.config import settings


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://192.168.0.32:8081/Authentication/SignIn')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://0.0.0.0:8081/Authentication/SignIn')


class AccountRabbitHelper:
    @classmethod
    async def validate_token(cls, token: str = Depends(oauth2_scheme)):
        response: bool = await rabbit_mq_client.call_and_wait_for_response(
            body=token,
            routing_key=ROUTING_KEY_CHECK_TOKEN,
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
        decoded: dict = await cls.decoded_token(token)

        current_roles = decoded.get('roles')

        for i in range(len(current_roles)):
            for j in range(len(roles)):
                if current_roles[i] == roles[j]:
                    return
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    

    @classmethod
    async def check_doctor(cls, doctor_id: uuid.UUID):
        response: bool = await rabbit_mq_client.call_and_wait_for_response(
            body=str(doctor_id),
            routing_key=ROUTING_KEY_CHECK_DOCTOR,
        )

        if response is not True:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=response
            )
        
    @classmethod
    async def check_pacient(cls, pacient_id: uuid.UUID):
        response = await rabbit_mq_client.call_and_wait_for_response(
            body=str(pacient_id), 
            routing_key=ROUTING_KEY_CHECK_PACIENT
        )

        if response is not True:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=response
            )
