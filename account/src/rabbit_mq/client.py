from src.rabbit_mq.base import RabbitMqBase, ROUTING_KEY_DELETE_TIMETABLE_DOCTOR

from aio_pika.abc import AbstractIncomingMessage, AbstractChannel
from aio_pika import Message

from fastapi.exceptions import HTTPException

from typing import Any, Callable


class RabbitMqClient(RabbitMqBase):
    async def publish_message(
        self, 
        channel: AbstractChannel,
        body: bytes,
        routing_key: str,
        correlation_id: str | None,
        reply_to: str | None
    ):
        await channel.default_exchange.publish(
            Message(
                body=body,
                correlation_id=correlation_id,
                reply_to=reply_to
            ),
            routing_key=routing_key
        )


    async def call(self, body: str):
        await self.connect()
        async with self.connection:
            channel = await self.connection.channel()

            await self.publish_message(
                channel=channel,
                body=body,
                routing_key=ROUTING_KEY_DELETE_TIMETABLE_DOCTOR
            )
        await self.close()


    async def pocess_message(
        message: AbstractIncomingMessage,
        channel: AbstractChannel,
        handler: Callable[[Any], bytes],
        *handler_args
    ):
        async with message.process():
            try:
                response = await handler(*handler_args)
            except HTTPException as e:
                response = str(e).encode()

            if message.reply_to:
                await channel.default_exchange.publish(
                    Message(
                        body=response,
                        correlation_id=message.correlation_id
                    ),
                    routing_key=message.reply_to
                )