from typing import Optional

from pydantic import Field
from pydantic.types import PositiveInt
from pydantic_settings import BaseSettings

from .constants import CacheRedisMode


class CacheRedisModeSettings(BaseSettings):
    deployment_mode: CacheRedisMode = Field(
        default=...,
        description="Redis mode",
        validation_alias="CACHE_DEPLOYMENT_MODE"
    )


class CacheRedisSettings(CacheRedisModeSettings):
    host: str = Field(
        default=...,
        description="Redis cluster host address",
        validation_alias="CACHE_HOST"
    )
    port: PositiveInt = Field(
        default=6379,
        description="Redis cluster port number",
        validation_alias="CACHE_PORT"
    )
    max_connections: PositiveInt = Field(
        default=10,
        description="Maximum number of connections in the pool",
        validation_alias="CACHE_MAX_CONNECTIONS"
    )
    socket_timeout: PositiveInt = Field(
        default=5,
        description="Socket timeout in seconds",
        validation_alias="CACHE_SOCKET_TIMEOUT"
    )
    socket_connect_timeout: PositiveInt = Field(
        default=5,
        description="Socket connection timeout in seconds",
        validation_alias="CACHE_SOCKET_CONNECT_TIMEOUT"
    )
    socket_keepalive: bool = Field(
        default=True,
        description="Enable socket keepalive",
        validation_alias="CACHE_SOCKET_KEEPALIVE"
    )
    health_check_interval: PositiveInt = Field(
        default=10,
        description="Health check interval in seconds",
        validation_alias="CACHE_HEALTH_CHECK_INTERVAL"
    )
    retry_max_attempts: PositiveInt = Field(
        default=3,
        description="Maximum number of retry attempts",
        validation_alias="CACHE_RETRY_MAX_ATTEMPTS"
    )
    
    @property
    def build_uri(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class CacheRedisClusterSettings(CacheRedisSettings):
    db: Optional[int] = Field(
        default=0,
        validation_alias="CACHE_DB"
    )
    read_from_replicas: bool = Field(
        default=True,
        description="Allow reading from replica nodes",
        validation_alias="CACHE_READ_FROM_REPLICAS"
    )
    require_full_coverage: bool = Field(
        default=False,
        description="Require full cluster coverage",
        validation_alias="CACHE_REQUIRE_FULL_COVERAGE"
    )
    
    def validate_cluster_db(self, value: int | None) -> int | None:
        if value is not None or value != 0:
            raise ValueError("redis.exceptions.RedisClusterException: Argument 'db' must be 0 or None in cluster mode")
        
        return value


class CacheRedisSingleNodeSettings(CacheRedisSettings):
    db: int = Field(
        default=0,
        ge=0,
        le=15,
        description="Redis database number (0-15)",
        validation_alias="CACHE_DB"
    )
    retry_on_timeout: bool = Field(
        default=True,
        description="Retry commands on timeout",
        validation_alias="CACHE_RETRY_ON_TIMEOUT"
    )
