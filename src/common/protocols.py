from typing import Protocol, runtime_checkable


@runtime_checkable
class BaseRepository(Protocol):
    async def healthcheck(self) -> tuple[bool, str | None]:
        ...
