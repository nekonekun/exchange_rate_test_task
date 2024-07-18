from typing import Iterable, Protocol


class CacheError(Exception):
    """Generic error"""


class CacheProtocol(Protocol):
    async def get(self, name: str) -> str: ...
    async def set(self, name: str, value: str, *args, **kwargs) -> str: ...
    async def keys(self, pattern: str, *args, **kwargs) -> Iterable[str]: ...
