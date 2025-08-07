from typing import Self

from pydantic import Field, model_validator, field_validator
from pydantic_settings import BaseSettings

from .contants import BrokerKafkaAcks


class BrokerKafkaSettings(BaseSettings):
    """Base settings for Kafka."""
    
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
    """Consumer settings for Kafka."""
    
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
    # enable_auto_commit: bool = Field(
    #     default=...,
    #     description="Kafka enable auto commit",
    #     validation_alias="BROKER_ENABLE_AUTO_COMMIT"
    # )
    max_poll_records: int = Field(
        default=100,
        ge=1,
        le=500,
        description="Kafka max poll records",
        validation_alias="BROKER_MAX_POLL_RECORDS"
    )
    max_poll_interval_ms: int = Field(
        default=(5*60*1000),
        description="Kafka max poll interval ms",
        validation_alias="BROKER_MAX_POLL_INTERVAL_MS"
    )
    heartbeat_interval_ms: int = Field(
        default=(15*1000),
        description="Kafka heartbeat interval ms",
        validation_alias="BROKER_HEARTBEAT_INTERVAL_MS"
    )
    session_timeout_ms: int = Field(
        default=(90*1000),
        description="Kafka session timeout ms",
        validation_alias="BROKER_SESSION_TIMEOUT_MS"
    )
    consumer_timeout_ms: int = Field(
        default=200,
        description="Kafka consumer timeout ms",
        validation_alias="BROKER_CONSUMER_TIMEOUT_MS"
    )
    # rebalance_timeout_ms: int = Field(
    #     default=...,
    #     description="Kafka rebalance timeout ms",
    #     validation_alias="BROKER_REBALANCE_TIMEOUT_MS"
    # )
    # isolation_level: str = Field(
    #     default=...,
    #     description="Kafka isolation level",
    #     validation_alias="BROKER_ISOLATION_LEVEL"
    # )
    
    @field_validator("topics", mode="before")
    @classmethod
    def validate_topics(cls, value: str) -> list[str]:
        """Validate topics."""
        return value.split(",") if value.find(",") > 0 else [value]
        
    @model_validator(mode="after")
    def validate_kafka_consumer_timeouts(self) -> Self:
        """Validate Kafka consumer timeouts.
        
        - pool timeout -> session timeout should end before pool interval
        - each session must have at least 3 heartbeat to ensure consumers it's alive
        """
        if not (
            self.max_poll_interval_ms > self.session_timeout_ms
            and self.session_timeout_ms / self.heartbeat_interval_ms >= 3
        ):
            raise ValueError("Kafka consumer timeouts are not valid")
        return self


class BrokerKafkaProducerSettings(BrokerKafkaSettings):
    """Producer settings for Kafka."""
    
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
