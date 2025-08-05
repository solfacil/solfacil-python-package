from abc import ABC, abstractmethod

from .settings import BrokerKafkaConsumerSettings, BrokerKafkaProducerSettings


class BrokerAdapterAbstract(ABC):
    
    @abstractmethod
    def __init__(
        self,
        producer_settings: BrokerKafkaProducerSettings | None = None,
        consumer_settings: BrokerKafkaConsumerSettings | None = None,
    ) -> None:
        ...
    
    @abstractmethod
    def config(self) -> "BrokerAdapterAbstract":
        ...
        
    @abstractmethod
    def connect(self) -> None:
        ...
    
    @abstractmethod
    def disconnect(self) -> None:
        ...
