from aio_pika.abc import AbstractRobustChannel
from aio_pika import connect_robust, Message


class RabbitMqBase:
    def __init__(self, rabbit_url='amqp://guest:guest@localhost/'):
        self.rabbit_url = rabbit_url
        self.connection: AbstractRobustChannel = None 

    async def connect(self):
        if self.connection is None or self.connection.is_closed:
            self.connection = await connect_robust(self.rabbit_url)
        return self.connection
    
    async def close(self):
        if self.connection is not None and not self.connection.is_closed:
            await self.connection.close()

    async def _publish_message(
        self, 
        channel: AbstractRobustChannel,
        body: bytes,
        routing_key: str 
    ):
        await channel.default_exchange.publish(
            Message(
                body=body
            ),
            routing_key=routing_key
        )