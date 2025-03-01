import asyncio
from aio_pika import connect_robust
from src.core.config import settings


async def consume_rabbitmq():
        try:
            await connect_robust(settings.rabbit_mq_url)

            print('Успешное подключение к RabbitMQ')
        except Exception as e:
            print(f'Ошибка подключения к RabbitMQ: {e}. Переподключение через 5 секунд...')
            await asyncio.sleep(5)