
from typing import Any
from .cluster import RedisClusterAdapter


class CacheRepository:
    def __init__(self, adapter: RedisClusterAdapter) -> None:
        self._cache = adapter
    
    async def set(self, key: str, value: Any) -> bool:
        return await self._cache.set(key, value)
    
    async def get(self, key: str) -> None | Any:
        return await self._cache.get(key)
    
    async def delete(self, keys: list[str]) -> int:
        return await self._cache.delete(keys)
    
    async def exists(self, keys: list[str]) -> int:
        return await self._cache.exists(keys)
    
    async def expire(self, key: str, time: int) -> bool:
        return await self._cache.expire(key, time)
    
    async def ttl(self, key: str) -> int:
        return await self._cache.ttl(key)
    
    async def healthcheck(self) -> bool:
        return await self._cache.healthcheck()
