from typing import Protocol

from pydantic import BaseModel


class KickMessage(BaseModel):
    requested_by: int = 0


class PublisherProtocol(Protocol):
    async def publish(self, message: BaseModel, **kwargs): ...
