from typing import Protocol, Any


class CacheProtocol(Protocol):
    def __init__(self, adapter) -> None:
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
    
    async def healthcheck(self) -> bool:
        ...
