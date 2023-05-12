from celery import Celery
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

from app.config import (
    logger,

    MTPROTO_TOKEN,
    MTPROTO_API_ID,
    MTPROTO_API_HASH,

    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
)
from app.services import scrape_message


celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND
celery.autodiscover_tasks()


@celery.task(name='scrape_channel_task')
def scrape_channel_task(
    channel_link: str,
    offset: int = 0,
    limit: int | None = None,
    min_characters: int = 280,
    reverse: bool = False
) -> bool:
    logger.info(f'start scrape for {channel_link=}')
    client = TelegramClient(StringSession(MTPROTO_TOKEN), MTPROTO_API_ID, MTPROTO_API_HASH)
    client.start()
    client.parse_mode = 'html'

    channel = client.get_entity(channel_link)
    for message in client.iter_messages(channel, add_offset=offset, limit=limit, reverse=reverse):
        scrape_message(
            min_characters=min_characters,
            message=message,
            channel=channel
        )
    return True