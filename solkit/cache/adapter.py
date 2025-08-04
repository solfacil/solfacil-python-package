from contextlib import asynccontextmanager
from typing import Any
import logging

from redis.asyncio.connection import ConnectionPool
from redis.asyncio.cluster import RedisCluster
from redis.asyncio.client import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff

from .settings import CacheRedisClusterSettings, CacheRedisModeSettings, CacheRedisSingleNodeSettings
from .constants import CacheRedisMode

logger = logging.getLogger(__name__)


class CacheRedisAdapter:
    
    @classmethod
    def single_node_config(cls) -> "CacheRedisAdapter":
        settings = CacheRedisSingleNodeSettings()
        return cls(settings)
    
    @classmethod
    def cluster_config(cls) -> "CacheRedisAdapter":
        settings = CacheRedisClusterSettings()
        return cls(settings)
    
    @classmethod
    def config(cls) -> "CacheRedisAdapter":
        cache_mode_settings = CacheRedisModeSettings()
        return (
            cls.cluster_config()
            if cache_mode_settings.deployment_mode == CacheRedisMode.CLUSTER 
            else cls.single_node_config()
        )
        
    def __init__(self, settings: CacheRedisClusterSettings | CacheRedisSingleNodeSettings) -> None:
        # self._connection_pool: ConnectionPool | None = None
        self._single_node_connection: Redis | None = None
        self._cluster_connection: RedisCluster | None = None
        self._settings = settings
        
    @property
    def __retry_config(self) -> dict[str, Any]:
        retry_config = {
            'retry': Retry(ExponentialBackoff(), retries=2),
            'retry_on_error': [ConnectionError, TimeoutError],
        }
        return retry_config
    
    @property
    def __common_config(self) -> dict[str, Any]:
        common_config = {
            'host': self._settings.host,
            'port': self._settings.port,
            'db': self._settings.db,
            'socket_timeout': self._settings.socket_timeout,
            'socket_keepalive': self._settings.socket_keepalive,
            'socket_connect_timeout': self._settings.socket_connect_timeout,
            'max_connections': self._settings.max_connections,
            'health_check_interval': self._settings.health_check_interval,
        }
        return common_config
    
    @property
    def __cluster_config(self) -> dict[str, Any]:
        cluster_config = {
            **self.__common_config,
            **self.__retry_config,
            'read_from_replicas': self._settings.read_from_replicas,
            'require_full_coverage': self._settings.require_full_coverage,
        }
        return cluster_config
    
    @property
    def __single_node_config(self) -> dict[str, Any]:
        single_node_config = {
            **self.__common_config,
            'retry_on_timeout': self._settings.retry_on_timeout,
        }
        return single_node_config
    
    def __create_cluster_connection(self) -> RedisCluster:
        self._cluster_connection = RedisCluster(**self.__cluster_config)
        
    def __create_single_node_connection(self) -> Redis:
        self._connection_pool = ConnectionPool(**self.__single_node_config)
        self._single_node_connection = Redis(connection_pool=self._connection_pool)
        # self._single_node_connection = Redis(**self.__single_node_config)
         
    async def connect(self) -> None: 
        logger.info(f"[ADAPTER][CACHE][CONNECTION URI: {self._settings.build_uri}]")
        logger.info(f"[ADAPTER][CACHE][CONNECTION MODE: {self._settings.deployment_mode.value.upper()}]")
        if self._settings.deployment_mode == CacheRedisMode.CLUSTER:
            self.__create_cluster_connection()
            logger.info(f"[ADAPTER][CACHE][CONNECTION ACTIVE: {await self._cluster_connection.ping()}]")
            logger.info(f"[ADAPTER][CACHE][CLUSTER NODES: {self._cluster_connection.get_nodes()}]")
        else:
            self.__create_single_node_connection()
            logger.info(f"[ADAPTER][CACHE][CONNECTION ACTIVE: {await self._single_node_connection.ping()}]")
            logger.info(f"[ADAPTER][CACHE][CONNECTION POOL ACTIVE: {self._connection_pool.can_get_connection()}]")
        
    async def __disconnect_cluster_connection(self) -> None:
        if self._cluster_connection:
            await self._cluster_connection.aclose()
            self._cluster_connection = None
            
    async def __disconnect_single_node_connection(self) -> None:
        if self._single_node_connection:
            await self._single_node_connection.aclose()
            self._single_node_connection = None

    async def disconnect(self) -> None:
        if self._settings.deployment_mode == CacheRedisMode.CLUSTER:
            await self.__disconnect_cluster_connection()
        else:
            await self.__disconnect_single_node_connection()
        logger.info("[ADAPTER][CACHE][DISCONNECTED]")
    
    @asynccontextmanager
    async def get_session(self):
        redis_connection = (
            self._cluster_connection
            if self._settings.deployment_mode == CacheRedisMode.CLUSTER
            else self._single_node_connection
        )
        async with redis_connection as session:
            yield session
