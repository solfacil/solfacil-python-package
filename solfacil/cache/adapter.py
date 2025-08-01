import logging
from contextlib import asynccontextmanager
from typing import Any

from redis.asyncio.cluster import RedisCluster
from redis.asyncio.client import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.connection import ConnectionPool

from .settings import CacheRedisClusterSettings, CacheRedisModeSettings, CacheRedisSingleNodeSettings
from .constants import CacheRedisMode

logger = logging.getLogger(__name__)


class CacheRedisAdapter:
    
    @staticmethod
    def __get_config(mode: CacheRedisModeSettings) -> CacheRedisClusterSettings | CacheRedisSingleNodeSettings:
        return (
            CacheRedisClusterSettings() 
            if mode.deployment_mode == CacheRedisMode.CLUSTER 
            else CacheRedisSingleNodeSettings()
        )
    
    @classmethod
    def config(cls) -> "CacheRedisAdapter":
        cache_mode_settings = CacheRedisModeSettings()
        cache_adapter_settings = cls.__get_config(cache_mode_settings)
        logger.info(f"[ADAPTER][CACHE COMMECTION URI: {cache_adapter_settings.build_uri}]")
        return cls(cache_adapter_settings)
        
    def __init__(self, settings: CacheRedisClusterSettings | CacheRedisSingleNodeSettings) -> None:
        logger.info("[ADAPTER][CACHE CREATED]")
        self._connection_pool: ConnectionPool | None = None
        self._redis: RedisCluster | Redis | None = None
        self._settings = settings
    
    @property
    def _common_config(self) -> dict[str, Any]:
        retry_config = Retry(ExponentialBackoff(), retries=2)
        
        common_config = {
            'host': self._settings.host,
            'port': self._settings.port,
            'socket_timeout': self._settings.socket_timeout,
            'socket_keepalive': self._settings.socket_keepalive,
            'socket_connect_timeout': self._settings.socket_connect_timeout,
            'max_connections': self._settings.max_connections,
            'health_check_interval': self._settings.health_check_interval,
            'retry': retry_config,
            'retry_on_error': [ConnectionError, TimeoutError],
        }
        return common_config
    
    @property
    def cluster_config(self) -> dict[str, Any]:
        cluster_config = {
            **self._common_config,
            'require_full_coverage': self._settings.require_full_coverage,
            'cluster_error_retry_attempts': self._settings.cluster_error_retry_attempts,
        }
        return cluster_config

    @property
    def single_node_config(self) -> dict[str, Any]:
        single_node_config = {
            **self._common_config,
            'retry_on_timeout': self._settings.retry_on_timeout,
        }
        return single_node_config
    
    def __create_cluster_connection(self) -> RedisCluster:
        logger.info(f"[ADAPTER][CACHE][CONNECTION MODE: {CacheRedisMode.CLUSTER.value.upper()}]")
        return RedisCluster(**self.cluster_config)
    
    def __create_single_node_connection_pool(self):
        logger.info(f"[ADAPTER][CACHE][CONNECTION POOL: {self._settings.max_connections}]")
        self._connection_pool = ConnectionPool(**self.single_node_config)
    
    def __create_single_node_connection(self) -> Redis:
        logger.info(f"[ADAPTER][CACHE][CONNECTION MODE: {CacheRedisMode.SINGLE_NODE.value.upper()}]")
        return Redis(connection_pool=self._connection_pool)
    
    async def connect(self) -> None:
        self._redis = (
            self.__create_cluster_connection() 
            if self._settings.deployment_mode == CacheRedisMode.CLUSTER 
            else self.__create_single_node_connection_pool()
        )
        logger.info(f"[ADAPTER][CACHE][CONNECTION ACTIVE: {await self._redis.ping()}]")
    
    async def __disconnect_cluster_connection(self) -> None:
        if self._redis:
            await self._redis.aclose()
            self._redis = None
            logger.info("[ADAPTER][CACHE][DISCONNECTED]")
    
    async def __disconnect_single_node_connection(self) -> None:
        if self._redis:
            await self._redis.close()
            self._redis = None
            logger.info("[ADAPTER][CACHE][DISCONNECTED]")
        
        if self._connection_pool:
            await self._connection_pool.aclose()
            self._connection_pool = None
            logger.info("[ADAPTER][CACHE][CONNECTION POOL CLOSED]")

    async def disconnect(self) -> None:
        if self._settings.deployment_mode == CacheRedisMode.CLUSTER:
            await self.__disconnect_cluster_connection()
        else:
            await self.__disconnect_single_node_connection()

    @asynccontextmanager
    async def get_session(self):
        async with self._redis as session:
            yield session
