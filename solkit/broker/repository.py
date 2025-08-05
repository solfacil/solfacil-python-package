from .adapter import BrokerKafkaAdapter


class BrokerRepository:
    def __init__(self, adapter: BrokerKafkaAdapter) -> None:
        self._adapter = adapter
    
    async def produce(self, topic: str, message: str) -> None:
        return await self._adapter._producer.send_and_wait(topic, message)
    
