from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractQueue
from aio_pika import connect_robust, Message

from src.core.config import settings

ROUTING_KEY_DELETE_TIMETABLE_DOCTOR = 'delete-timetable-doctor'

class RabbitMqBase:
    def __init__(self, rabbit_url=settings.rabbit_mq_url):
        self.rabbit_url = rabbit_url
        self.connection: AbstractConnection = None 
        self._channel: AbstractChannel | None = None


    async def connect(self) -> AbstractConnection:
        if self.connection is None or self.connection.is_closed:
            self.connection = await connect_robust(self.rabbit_url)
        return self.connection

    
    async def close(self) -> None:
        if self.connection is not None and not self.connection.is_closed:
            await self.connection.close()
