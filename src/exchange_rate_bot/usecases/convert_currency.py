from decimal import Decimal

from exchange_rate_bot.usecases.protocols.cache import CacheProtocol
from exchange_rate_bot.usecases.protocols.currency import CurrencyInfo


class ConvertCurrencyError(Exception):
    """Generic error"""


class CurrencyNotFoundError(ConvertCurrencyError):
    """Currency not found"""


class ConvertCurrency:
    def __init__(self, cache: CacheProtocol):
        self.cache = cache

    async def parse_currency(self, currency: str) -> CurrencyInfo:
        if currency == 'RUB':
            return CurrencyInfo(
                num_code=0,
                char_code='RUB',
                nominal=1,
                name='Российский рубль',
                value=Decimal(1),
                vunit_rate=Decimal(1),
            )
        else:
            from_info = await self.cache.get(f'currency:{currency}')
            if from_info is None:
                raise CurrencyNotFoundError
            return CurrencyInfo.model_validate_json(from_info)

    async def __call__(self, from_currency: str, to_currency: str, amount: float) -> Decimal:
        from_info = await self.parse_currency(from_currency)
        to_info = await self.parse_currency(to_currency)
        return Decimal(amount) * from_info.vunit_rate / to_info.vunit_rate
