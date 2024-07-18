import os

from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka
from faststream import FastStream
from faststream.redis import RedisBroker

from exchange_rate_bot.main.ioc import MainProvider
from exchange_rate_bot.queue.routers import router


def create_app():
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_db = int(os.getenv('REDIS_QUEUE_DB', '1'))

    broker = RedisBroker(
        host=redis_host,
        port=redis_port,
        db=redis_db,
    )
    broker.include_router(router)
    app = FastStream(broker)
    container = make_async_container(MainProvider())
    setup_dishka(container=container, app=app)
    return app
