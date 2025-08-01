from typing import Any, Protocol, runtime_checkable

from redis.asyncio.cluster import RedisCluster
from redis.asyncio.client import Redis


@runtime_checkable
class CacheRepositoryProtocol(Protocol):
    def __init__(self, cache_session: RedisCluster | Redis) -> None:
        ...
    
    async def set(self, key: str, value: Any) -> bool:
        ...
    
    async def get(self, key: str) -> None | Any:
        ...
    
    async def delete(self, keys: list[str]) -> int:
        ...
    
    async def exists(self, keys: list[str]) -> int:
        ...
    
    async def expire(self, key: str, time: int) -> bool:
        ...
    
    async def ttl(self, key: str) -> int:
        ...
    
    async def healthcheck(self) -> tuple[bool, str | None]:
        ...
