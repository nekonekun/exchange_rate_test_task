import asyncio
import os

from aiogram import Dispatcher, Bot
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from exchange_rate_bot.main.ioc import MainProvider
from exchange_rate_bot.telegram.routers import router


async def start_bot():
    token = os.getenv('BOT_TOKEN')
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    container = make_async_container(MainProvider())
    setup_dishka(container=container, router=dispatcher)
    bot = Bot(token=token)
    try:
        await dispatcher.start_polling(bot)
    except asyncio.CancelledError:
        await bot.session.close()


def main():
    asyncio.run(start_bot())


if __name__ == '__main__':
    main()
