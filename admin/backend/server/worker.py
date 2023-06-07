from celery import Celery
from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession

from .config import (
    logger,

    MTPROTO_TOKEN,
    MTPROTO_API_ID,
    MTPROTO_API_HASH,

    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND
)
from .utils.telegram_scraper import (
    scrape_message,
    scrape_message_async
)
from .services.telegram_scraper import get_telegram_scraper_by_channel_link


celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


@celery.task
def scrape_telegram_channel_task(
    channel_link: str,
    offset: int = 0,
    limit: int | None = None,
    min_characters: int = 280,
    reverse: bool = False
) -> bool:
    logger.info(f'start scrape for {channel_link=} {offset=} {limit=}')
    client = TelegramClient(
        session=StringSession(MTPROTO_TOKEN),
        api_id=MTPROTO_API_ID,
        api_hash=MTPROTO_API_HASH
    )
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


@celery.task
def listen_for_new_channels_messages(channel_username_list: list[str]):
    with TelegramClient(StringSession(MTPROTO_TOKEN), MTPROTO_API_ID, MTPROTO_API_HASH) as client:
        client.parse_mode = 'html'

        @client.on(events.NewMessage(chats=channel_username_list))
        async def new_message_listener(event):
            logger.info('start scraping new message')
            message = event.message
            channel = await event.get_chat()

            logger.debug(f'channel username {channel.username}')
            telegram_scraper = await get_telegram_scraper_by_channel_link(f'https://t.me/{channel.username}')
            min_characters = telegram_scraper.min_characters

            await scrape_message_async(
                min_characters=min_characters,
                message=message,
                channel=channel
            )

        client.run_until_disconnected()
