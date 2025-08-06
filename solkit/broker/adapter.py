import logging

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from .settings import BrokerKafkaConsumerSettings, BrokerKafkaProducerSettings

logger = logging.getLogger(__name__)


class BrokerKafkaAdapter:
    
    # @classmethod
    # def config_consumer(cls) -> "BrokerKafkaAdapter":
    #    consumer_settings = BrokerKafkaConsumerSettings()
    #    return cls(consumer_settings=consumer_settings)
    
    @classmethod
    def producer_config(cls) -> "BrokerKafkaAdapter":
        producer_settings = BrokerKafkaProducerSettings()
        return cls(producer_settings=producer_settings)
    
    # @classmethod
    # def config(cls) -> "BrokerKafkaAdapter":
    #    producer_settings = BrokerKafkaProducerSettings()
    #    consumer_settings = BrokerKafkaConsumerSettings()
    #    return cls(producer_settings=producer_settings, consumer_settings=consumer_settings)
    
    def __init__(
        self,
        producer_settings: BrokerKafkaProducerSettings | None = None,
        # consumer_settings: BrokerKafkaConsumerSettings | None = None,
    ) -> None:
        self._producer_settings = producer_settings
        # self._consumer_settings = consumer_settings
        self._producer: AIOKafkaProducer | None = None
        # self._consumer: Optional[AIOKafkaConsumer] = None

    def __create_producer(self) -> None:
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._producer_settings.bootstrap_servers,
            request_timeout_ms=self._producer_settings.request_timeout_ms,
            acks=self._producer_settings.acks,
            connections_max_idle_ms=self._producer_settings.connections_max_idle_ms,
        )
    
    # def __create_consumer(self) -> None:
    #    self._consumer = AIOKafkaConsumer(
    #        bootstrap_servers=self._consumer_settings.bootstrap_servers,
    #        request_timeout_ms=self._consumer_settings.request_timeout_ms,
    #        group_id=self._consumer_settings.group_id,
    #        topics=self._consumer_settings.topics,
    #        max_poll_records=self._consumer_settings.max_poll_records,
    #        enable_auto_commit=self._consumer_settings.enable_auto_commit,
    #    )
    
    async def __start_producer(self) -> None:
        self.__create_producer()
        await self._producer.start()
    
    # async def __start_consumer(self) -> None:
    #    self.__create_consumer()
    #    await self._consumer.start()
    #    await self._consumer.topics()
    
    async def connect(self) -> None:
        if self._producer_settings is not None:
            await self.__start_producer()
        # if self._consumer_settings is not None:
        #    await self.__start_consumer()
    
    async def __disconnect_producer(self) -> None:
        if self._producer is not None:
            await self._producer.stop()
            self._producer = None
        
    async def disconnect(self) -> None:
        if self._producer is not None:
            await self.__disconnect_producer()
        # if self._consumer is not None:
        # await self._consumer.stop()
