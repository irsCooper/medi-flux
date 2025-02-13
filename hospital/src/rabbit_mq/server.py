import asyncio
from functools import partial
import uuid
from aio_pika.abc import AbstractIncomingMessage
from aio_pika import RobustChannel, Message, connect_robust
from fastapi import HTTPException

from src.core.db_helper import db
from src.core.config import settings


# async def check_hospital_room(
#     message: AbstractIncomingMessage,
#     channel: RobustChannel
# ):
#     async with message.process():
#         doctor_id = message.body.decode()
#         try:
#             async with db.session_dependency() as session:
#                 await DoctorSrvice.get_doctor(
#                     uuid.UUID(doctor_id),
#                     session
#                 )
#                 response = b'\x01'
#         except HTTPException:
#             response = b'\x00'
        
#         if message.reply_to:
#             await channel.default_exchange.publish(
#                 Message(
#                     body=response,
#                     correlation_id=message.correlation_id
#                 ),
#                 routing_key=message.reply_to
#             )