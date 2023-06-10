from arq.connections import RedisSettings

from .tasks import (
    scrape_telegram_channel_job,
    listen_for_new_telegram_channel_messages_job
)


class WorkerSettings:
    functions = [
        scrape_telegram_channel_job,
        listen_for_new_telegram_channel_messages_job
    ]
    redis_settings = RedisSettings(
        host='redis'
    )
    job_timeout = 3600 * 24 * 365 * 10 # 10 years
    allow_abort_jobs = True
