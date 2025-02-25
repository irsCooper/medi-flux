import uuid

from fastapi import HTTPException, status


from src.rabbit_mq.base import ROUTING_KEY_CHECK_HOSPITAL
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

        print(response)
        
        # if response == False:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=response
        #     )
