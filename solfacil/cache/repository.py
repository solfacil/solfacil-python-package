
from typing import Any
from .cluster import CacheRedisAdapter

from redis.exceptions import RedisError, ConnectionError


class CacheRepository:
    def __init__(self, cache_session: CacheRedisAdapter) -> None:
        self._cache_session = cache_session
    
    async def set(self, key: str, value: Any) -> bool:
        return await self._cache_session.set(key, value)
    
    async def get(self, key: str) -> None | Any:
        return await self._cache_session.get(key)
    
    async def delete(self, keys: list[str]) -> int:
        return await self._cache_session.delete(keys)
    
    async def exists(self, keys: list[str]) -> int:
        return await self._cache_session.exists(keys)
    
    async def expire(self, key: str, time: int) -> bool:
        return await self._cache_session.expire(key, time)
    
    async def ttl(self, key: str) -> int:
        return await self._cache_session.ttl(key)
    
    async def healthcheck(self) -> bool:
        try:
            await self._cache_session.ping()
            return True
        except (RedisError, ConnectionError):
            return False
