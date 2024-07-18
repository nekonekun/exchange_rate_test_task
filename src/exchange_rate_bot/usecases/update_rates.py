from exchange_rate_bot.usecases.protocols.currency import CurrencyProtocol, CurrencyError
from exchange_rate_bot.usecases.protocols.cache import CacheProtocol, CacheError


class UpdateRatesError(Exception):
    """Generic error"""


class UpdateRates:
    def __init__(self, currency: CurrencyProtocol, cache: CacheProtocol):
        self.currency = currency
        self.cache = cache

    async def __call__(self):
        try:
            currencies_info_list = await self.currency.get_actual_rates()
        except CurrencyError as e:
            raise UpdateRatesError(e)

        for element in currencies_info_list:
            try:
                await self.cache.set(
                    name=f'currency:{element.char_code}',
                    value=element.model_dump_json(),
                )
            except CacheError as e:
                raise UpdateRatesError(e)
