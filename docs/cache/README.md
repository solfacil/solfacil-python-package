
# Python Cache - Redis Adapter

## Usage

```python
# cache.py
from solfacil.cache import RedisClusterAdapter

redis_adapter = RedicsClusterAdapter.config()

async def get_cache_session():
    async with redis_adapter.get_session() as cache_session:
        yield cache_session
```

```python
# app.py
from adapters.cache.settings import cache_redis_adapter

async def lifespan(app: FastAPI):
    await cache_redis_adapter.connect()
    yield
    await cache_redis_adapter.disconnect()

def application() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan
    )
    return app

app = application()
```

```python
# route.py
from fastapi import APIRouter, Depends
from solfacil.cache import CacheRepository

from adapters.cache.settings import get_cache_session

router = APIRouter()

@router.get("/example")
async def example(
    cache_session = Depends(get_cache_session)
):
    service = ExampleService(CacheRepository(cache_session))
    return await service.process()
```
