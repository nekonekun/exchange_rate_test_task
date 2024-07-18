import os
from typing import AsyncIterable

from aiohttp import ClientSession
from dishka import Provider, alias, Scope, provide
from redis.asyncio import Redis

from exchange_rate_bot.adapters.central_bank import CentralBankAdapter
from exchange_rate_bot.usecases.protocols.cache import CacheProtocol
from exchange_rate_bot.usecases.protocols.currency import CurrencyProtocol
from exchange_rate_bot.usecases.convert_currency import ConvertCurrency
from exchange_rate_bot.usecases.get_all_rates import GetAllRates
from exchange_rate_bot.usecases.update_rates import UpdateRates


class MainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_cb_adapter(self) -> AsyncIterable[CentralBankAdapter]:
        async with ClientSession(base_url='http://www.cbr.ru/') as session:
            yield CentralBankAdapter(session=session)

    @provide(scope=Scope.APP)
    async def provide_currency_redis(self) -> AsyncIterable[Redis]:
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_db = int(os.getenv('REDIS_DB', '3'))
        redis_client = Redis(host=redis_host, port=redis_port, db=redis_db)
        yield redis_client
        await redis_client.close()

    currency_protocol = alias(source=CentralBankAdapter, provides=CurrencyProtocol)
    cache_protocol = alias(source=Redis, provides=CacheProtocol)

    convert_currency = provide(ConvertCurrency, scope=Scope.REQUEST)
    get_all_rates = provide(GetAllRates, scope=Scope.REQUEST)
    update_rates = provide(UpdateRates, scope=Scope.REQUEST)
