
from typing import Optional, List
from pydantic import Field
from pydantic.types import PositiveInt
from pydantic_settings import BaseSettings


class RedisClusterSettings(BaseSettings):
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
    db: int = Field(
        default=0,
        ge=0,
        le=15,
        description="Redis database number (0-15)",
        validation_alias="CACHE_DB"
    )
    
    # Connection Pool Settings
    max_connections: PositiveInt = Field(
        default=10,
        description="Maximum number of connections in the pool",
        validation_alias="CACHE_MAX_CONNECTIONS"
    )
    min_connections: PositiveInt = Field(
        default=1,
        description="Minimum number of connections in the pool",
        validation_alias="CACHE_MIN_CONNECTIONS"
    )
    
    # Connection timeout settings
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
    
    # Cluster-specific settings
    decode_responses: bool = Field(
        default=True,
        description="Automatically decode responses to strings",
        validation_alias="CACHE_DECODE_RESPONSES"
    )
    health_check_interval: PositiveInt = Field(
        default=30,
        description="Health check interval in seconds",
        validation_alias="CACHE_HEALTH_CHECK_INTERVAL"
    )
    retry_on_timeout: bool = Field(
        default=True,
        description="Retry commands on timeout",
        validation_alias="CACHE_RETRY_ON_TIMEOUT"
    )
    # retry_on_error: List[str] = Field(
    #     default=["ConnectionError", "TimeoutError"],
    #     description="List of error types to retry on"
    # )
    # max_attempts: PositiveInt = Field(
    #     default=3,
    #     description="Maximum number of retry attempts"
    # )
    
    # Cluster discovery settings
    cluster_nodes: Optional[List[str]] = Field(
        default=None,
        description="List of cluster node addresses (host:port)",
        validation_alias="CACHE_CLUSTER_NODES"
    )
    skip_full_coverage_check: bool = Field(
        default=False,
        description="Skip full cluster coverage check"
    )
    
    # Performance settings
    read_from_replicas: bool = Field(
        default=False,
        description="Allow reading from replica nodes",
        validation_alias="CACHE_READ_FROM_REPLICAS"
    )
    readonly: bool = Field(
        default=False,
        description="Set connection to read-only mode",
        validation_alias="CACHE_READONLY"
    )
