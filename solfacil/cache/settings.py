
from typing import Optional, List
from pydantic import BaseSettings, Field
from pydantic.types import PositiveInt


class RedisClusterSettings(BaseSettings):
    host: str = Field(
        default="localhost",
        description="Redis cluster host address"
    )
    port: PositiveInt = Field(
        default=6379,
        description="Redis cluster port number"
    )
    db: int = Field(
        default=0,
        ge=0,
        le=15,
        description="Redis database number (0-15)"
    )
    
    # Connection Pool Settings
    max_connections: PositiveInt = Field(
        default=10,
        description="Maximum number of connections in the pool"
    )
    min_connections: PositiveInt = Field(
        default=1,
        description="Minimum number of connections in the pool"
    )
    
    # Connection timeout settings
    socket_timeout: PositiveInt = Field(
        default=5,
        description="Socket timeout in seconds"
    )
    socket_connect_timeout: PositiveInt = Field(
        default=5,
        description="Socket connection timeout in seconds"
    )
    socket_keepalive: bool = Field(
        default=True,
        description="Enable socket keepalive"
    )
    
    # Cluster-specific settings
    decode_responses: bool = Field(
        default=True,
        description="Automatically decode responses to strings"
    )
    health_check_interval: PositiveInt = Field(
        default=30,
        description="Health check interval in seconds"
    )
    retry_on_timeout: bool = Field(
        default=True,
        description="Retry commands on timeout"
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
        description="List of cluster node addresses (host:port)"
    )
    skip_full_coverage_check: bool = Field(
        default=False,
        description="Skip full cluster coverage check"
    )
    
    # Performance settings
    read_from_replicas: bool = Field(
        default=False,
        description="Allow reading from replica nodes"
    )
    readonly: bool = Field(
        default=False,
        description="Set connection to read-only mode"
    )