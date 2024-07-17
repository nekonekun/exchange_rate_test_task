from decimal import Decimal
from typing import Protocol

from pydantic import BaseModel


class CurrencyError(Exception):
    """Generic error"""


class CurrencyInfo(BaseModel):
    num_code: int
    char_code: str
    nominal: int
    name: str
    value: Decimal
    vunit_rate: Decimal


class CurrencyProtocol(Protocol):
    async def get_actual_rates(self) -> list[CurrencyInfo]: ...
