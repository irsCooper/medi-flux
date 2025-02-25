import json
import uuid

from fastapi import HTTPException, status


from src.rabbit_mq.base import ROUTING_KEY_CHECK_HOSPITAL, ROUTING_KEY_CHECK_HOSPITAL_ROOM
from src.rabbit_mq.client import rabbit_mq_client


class HospitalRabbitHelper:
    @classmethod
    async def check_hospital(self, hospital_id: uuid.UUID):
        correlation_id = str(uuid.uuid4())

        await rabbit_mq_client.connect()
        channel = await rabbit_mq_client.create_channel()
        callback_queue = await rabbit_mq_client.create_queue(channel)

        response = await rabbit_mq_client.call_and_wait_for_response(
            channel=channel,
            body=str(hospital_id), 
            routing_key=ROUTING_KEY_CHECK_HOSPITAL,
            correlation_id=correlation_id,
            callback_queue=callback_queue
        )
        
        if response == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hospital not found"
            )
        
    @classmethod
    async def check_hospital_room(self, hospital_id: uuid.UUID, room: str):
        correlation_id = str(uuid.uuid4())

        await rabbit_mq_client.connect()
        channel = await rabbit_mq_client.create_channel()
        callback_queue = await rabbit_mq_client.create_queue(channel)

        data = json.dumps({
            'hospital_id': hospital_id,
            'room': room
        }, ensure_ascii=False)

        response: bool | str = await rabbit_mq_client.call_and_wait_for_response(
            channel=channel,
            body=data, 
            routing_key=ROUTING_KEY_CHECK_HOSPITAL_ROOM,
            correlation_id=correlation_id,
            callback_queue=callback_queue
        )
        
        if response is not True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response
            )
