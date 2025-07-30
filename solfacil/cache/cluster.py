import logging

from redis.asyncio.connection import ConnectionPool
from redis.asyncio.cluster import RedisCluster
from redis.exceptions import RedisError, ConnectionError

from .settings import RedisClusterSettings

logger = logging.getLogger(__name__)


class RedisClusterAdapter:
    
    @classmethod
    def config(cls) -> "RedisClusterAdapter":
        config = RedisClusterSettings()
        return cls(
            host=config.host,
            port=config.port,
            db=config.db,
            max_connections=config.max_connections,
        )
    
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        max_connections: int
    ) -> None:
        self.host = host
        self.port = port
        self.max_connections = max_connections
        
        self._pool: ConnectionPool | None = None
        self._redis: RedisCluster | None = None
    
    def __create_cluster_connection_pool(self) -> ConnectionPool:
        return ConnectionPool(
            host=self.host,
            port=self.port,
            max_connections=self.max_connections,
            # decode_responses=self.decode_responses,
            # health_check_interval=self.health_check_interval,
        )
    
    def __create_cluster_connection(self) -> RedisCluster:
        return RedisCluster(
            connection_pool=self._pool,
            # decode_responses=self.decode_responses
        )
    
    async def connect(self) -> None:
        self._pool = self.__create_cluster_connection_pool()
        self._redis = self.__create_cluster_connection()
    
    async def get_session(self) -> RedisCluster:
        return self._redis

    async def disconnect(self) -> None:
        if self._redis:
            await self._redis.close()
            self._redis = None
        
        if self._pool:
            await self._pool.disconnect()
            self._pool = None
    
    async def healthcheck(self) -> bool:
        try:
            await self._redis.ping()
            return True
        except (RedisError, ConnectionError):
            return False
