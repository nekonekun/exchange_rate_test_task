from dishka.integrations.faststream import FromDishka, inject
from faststream import Logger
from faststream.redis import RedisRouter

from exchange_rate_bot.usecases.protocols.publisher import KickMessage
from exchange_rate_bot.usecases.update_rates import UpdateRates

router = RedisRouter()


@router.subscriber('updater-channel')
@inject
async def update_rates_handler(
    msg: KickMessage,
    logger: Logger,
    update_rates: FromDishka[UpdateRates],
):
    if msg.requested_by:
        logger.info(f'Пользователь {msg.requested_by} запросил обновление курсов валют')
    else:
        logger.info('Обновление курсов валют запущено по расписанию')
    await update_rates()
