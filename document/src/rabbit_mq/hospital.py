import json
import uuid

from fastapi import HTTPException, status

from src.rabbit_mq.base import ROUTING_KEY_CHECK_HOSPITAL, ROUTING_KEY_CHECK_HOSPITAL_ROOM
from src.rabbit_mq.client import rabbit_mq_client


class HospitalRabbitHelper:
    @classmethod
    async def check_hospital_room(cls, hospital_id: uuid.UUID, room: str):
        data = json.dumps({
            'hospital_id': str(hospital_id),
            'room': room
        }, ensure_ascii=False)

        response: bool | str = await rabbit_mq_client.call_and_wait_for_response(
            body=data, 
            routing_key=ROUTING_KEY_CHECK_HOSPITAL_ROOM,
        )
        
        if response is not True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response
            )
