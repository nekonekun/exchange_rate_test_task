from exchange_rate_bot.usecases.protocols.cache import CacheProtocol, CacheError
from exchange_rate_bot.usecases.protocols.currency import CurrencyInfo


class GetAllRatesError(Exception):
    """Generic error"""


class GetAllRates:
    def __init__(self, cache: CacheProtocol):
        self.cache = cache

    async def __call__(self) -> list[CurrencyInfo]:
        currency_names = await self.cache.keys('currency:*')
        try:
            result = [
                CurrencyInfo.model_validate_json(await self.cache.get(currency_name))
                for currency_name in currency_names
            ]
        except CacheError as e:
            raise GetAllRatesError(e)
        return result
