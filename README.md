
# Solfacil Python Packages

## Redis

```python
from solfacil.redis import RedisClusterAdapter

redis_adapter = RedicsClusterAdapter.config()
redis_adapter.connect()

async def get_cache_session()
    async with redis_adapter.get_session() as cache_session:
        yield cache_session


@router.get(/some/path)
async def route(cache_session = Depends(get_cache_session)):
    service = ExampleService(CacheRepository(cache_session))
    return await service.work()
```
