from enum import StrEnum


class BrokerKafkaAcks(StrEnum):
    ALL = "all"
    ZERO = "0"
    ONE = "1"
