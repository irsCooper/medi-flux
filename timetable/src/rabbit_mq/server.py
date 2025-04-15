import uuid
import asyncio

from fastapi import HTTPException
from functools import partial
from aio_pika.abc import AbstractIncomingMessage
from aio_pika import RobustChannel, Message, connect_robust

from src.timetables.service import TimetableService
from src.core.db_helper import db
from src.core.config import settings


# TODO
async def delete_timetable_doctor(
    message: AbstractIncomingMessage,
    channel: RobustChannel
):
    async with message.process():
        doctor_id = message.body.decode()
        # try:
        #     async with db.session_dependency() as sessin:
                # await 


async def consume_rabbitmq():
        try:
            await connect_robust(settings.rabbit_mq_url)

            print('Успешное подключение к RabbitMQ')
        except Exception as e:
            print(f'Ошибка подключения к RabbitMQ: {e}. Переподключение через 5 секунд...')
            await asyncio.sleep(5)