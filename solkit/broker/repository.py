import json
from typing import Any, Callable

from .adapter import BrokerKafkaAdapter


class BrokerRepository:
    def __init__(self, adapter: BrokerKafkaAdapter) -> None:
        self._adapter = adapter
    
    @staticmethod
    def __parse_message(message: dict[str, Any]) -> bytes:
        return json.dumps(message).encode("utf-8")
    
    async def produce(self, topic: str, message: dict[str, Any]) -> None:
        return await self._adapter._producer.send_and_wait(topic, self.__parse_message(message))
    
    async def consume(self, func: Callable) -> None:
        async for message in self._adapter._consumer:
            await func(message)

    # async def healthcheck(self) -> None:
    #     producer = await self._adapter._producer.send_and_wait("healthcheck", "healthcheck")
    #     consumer = self._adapter._consumer.subscription()  # list topics subscribed
    #     consumer = self._adapter._consumer.assignment()  # list partitions assigned
    #     return producer and consumer
