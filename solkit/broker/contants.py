from enum import Enum


class BrokerKafkaAcks(Enum):
    """Valid values for Kafka Producer ACKS."""
    
    ALL = "all"
    ZERO = 0
    ONE = 1
