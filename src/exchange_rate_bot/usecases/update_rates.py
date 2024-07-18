from exchange_rate_bot.usecases.protocols.cache import CacheError, CacheProtocol
from exchange_rate_bot.usecases.protocols.currency import (
    CurrencyError,
    CurrencyProtocol,
)
from exchange_rate_bot.usecases.protocols.publisher import (
    KickMessage,
    PublisherProtocol,
)


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
            raise UpdateRatesError from e

        try:
            for element in currencies_info_list:
                await self.cache.set(
                    name=f'currency:{element.char_code}',
                    value=element.model_dump_json(),
                )
        except CacheError as e:
            raise UpdateRatesError from e


class KickUpdateRates:
    def __init__(self, publisher: PublisherProtocol):
        self.publisher = publisher

    async def __call__(self, requested_by: int):
        await self.publisher.publish(KickMessage(requested_by=requested_by))
