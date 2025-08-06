from pydantic import Field
from pydantic_settings import BaseSettings

from .contants import BrokerKafkaAcks


class BrokerKafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(
        default=...,
        description="Kafka bootstrap servers",
        validation_alias="BROKER_BOOTSTRAP_SERVERS"
    )
    request_timeout_ms: int = Field(
        default=5000,
        description="Kafka request timeout ms",
        validation_alias="BROKER_REQUEST_TIMEOUT_MS"
    )


class BrokerKafkaConsumerSettings(BrokerKafkaSettings):
    topics: list[str] = Field(
        default=...,
        description="Kafka topics",
        validation_alias="BROKER_TOPICS"
    )
    group_id: str = Field(
        default=...,
        description="Kafka group id",
        validation_alias="BROKER_GROUP_ID"
    )
    max_poll_records: int = Field(
        default=...,
        ge=1,
        le=500,
        description="Kafka max poll records",
        validation_alias="BROKER_MAX_POLL_RECORDS"
    )
    enable_auto_commit: bool = Field(
        default=...,
        description="Kafka enable auto commit",
        validation_alias="BROKER_ENABLE_AUTO_COMMIT"
    )
    max_poll_interval_ms: int = Field(
        default=...,
        description="Kafka max poll interval ms",
        validation_alias="BROKER_MAX_POLL_INTERVAL_MS"
    )
    rebalance_timeout_ms: int = Field(
        default=...,
        description="Kafka rebalance timeout ms",
        validation_alias="BROKER_REBALANCE_TIMEOUT_MS"
    )
    heartbeat_interval_ms: int = Field(
        default=...,
        description="Kafka heartbeat interval ms",
        validation_alias="BROKER_HEARTBEAT_INTERVAL_MS"
    )
    session_timeout_ms: int = Field(
        default=...,
        description="Kafka session timeout ms",
        validation_alias="BROKER_SESSION_TIMEOUT_MS"
    )
    consumer_timeout_ms: int = Field(
        default=...,
        description="Kafka consumer timeout ms",
        validation_alias="BROKER_CONSUMER_TIMEOUT_MS"
    )
    isolation_level: str = Field(
        default=...,
        description="Kafka isolation level",
        validation_alias="BROKER_ISOLATION_LEVEL"
    )
    
    def validate_timeout_constrains(self) -> None:
        pass


class BrokerKafkaProducerSettings(BrokerKafkaSettings):
    acks: BrokerKafkaAcks = Field(
        default=BrokerKafkaAcks.ALL,
        description="Kafka acks",
        validation_alias="BROKER_ACKS"
    )
    connections_max_idle_ms: int = Field(
        default=10000,
        description="Kafka connections max idle ms",
        validation_alias="BROKER_CONNECTIONS_MAX_IDLE_MS"
    )

    def parsed_acks(self) -> int | str:
        """Parse ACKS value to return 0 or 1 as int and 'all' as string."""
        return str(self.acks.value) if self.acks == BrokerKafkaAcks.ALL else int(self.acks.value)
