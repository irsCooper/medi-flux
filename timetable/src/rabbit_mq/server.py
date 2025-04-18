import uuid
import asyncio

from fastapi import HTTPException
from functools import partial
from aio_pika.abc import AbstractIncomingMessage
from aio_pika import RobustChannel, Message, connect_robust

from src.timetables.service import TimetableService
from src.core.db_helper import db
from src.core.config import settings


async def delete_timetable_doctor(
    message: AbstractIncomingMessage,
    channel: RobustChannel
):
    async with message.process():
        doctor_id = message.body.decode()
        try:
            async with db.session_factory() as session:
                await TimetableService.delete_timetables_for_doctor_id(
                    doctor_id=uuid.UUID(doctor_id), session=session
                )

                response = b'\x01'
        except HTTPException as e:
            response = str(e).encode('ascii', errors='ignore')
        
        if message.reply_to:
            await channel.default_exchange.publish(
                Message(
                    body=response,
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )

async def consume_rabbitmq():
        try:
            connection = await connect_robust(settings.rabbit_mq_url)
            channel = await connection.channel()

            delete_timetable_doctor_queue = await channel.declare_queue(
                'delete_timetable_doctor', auto_delete=True
            )

            await delete_timetable_doctor_queue.consume(partial(delete_timetable_doctor, channel=channel))
        except Exception as e:
            print(f'Ошибка подключения к RabbitMQ: {e}. Переподключение через 5 секунд...')
            await asyncio.sleep(5)