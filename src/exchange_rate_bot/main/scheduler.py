import os

from taskiq_faststream import BrokerWrapper
from taskiq_faststream import StreamScheduler
from taskiq.schedule_sources import LabelScheduleSource
from faststream.redis import RedisBroker

from exchange_rate_bot.usecases.protocols.publisher import KickMessage

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', '6379'))
redis_db = int(os.getenv('REDIS_QUEUE_DB', '1'))
schedule = os.getenv('SCHEDULE_CRON', '*/15 * * * *')

broker = RedisBroker(
    host=redis_host,
    port=redis_port,
    db=redis_db,
)
taskiq_broker = BrokerWrapper(broker)

taskiq_broker.task(
    message=KickMessage(),
    channel="updater-channel",
    schedule=[{
        "cron": schedule,
    }],
)

scheduler = StreamScheduler(
    broker=taskiq_broker,
    sources=[LabelScheduleSource(taskiq_broker)],
)
