from pydantic import HttpUrl, validate_arguments
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
from .services.telegram_scraper import (
    get_telegram_scraper_by_channel_link,
    get_telegram_scraper_list,
    set_telegram_scraper_task_id
)
from .services.telegram_updates_scraper_conf import (
    get_telegram_updates_scraper_conf,
    set_telegram_updates_scraper_task_id
)


celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


@celery.task
@validate_arguments
def scrape_telegram_channel_task(
    channel_link: HttpUrl,
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
@validate_arguments
def listen_for_new_telegram_channel_messages_task(channel_link_list: list[HttpUrl]):
    with TelegramClient(StringSession(MTPROTO_TOKEN), MTPROTO_API_ID, MTPROTO_API_HASH) as client:
        client.parse_mode = 'html'

        @client.on(events.NewMessage(chats=channel_link_list))
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


async def run_all_telegram_scrapers():
    telegram_scraper_list = await get_telegram_scraper_list()

    for telegram_scraper in telegram_scraper_list:
        if telegram_scraper.task_id:
            celery.control.revoke(telegram_scraper.task_id, terminate=True)

        task_result = scrape_telegram_channel_task.apply_async(kwargs={
            'channel_link': telegram_scraper.channel_link,
            'offset': telegram_scraper.offset,
            'limit': telegram_scraper.limit,
            'min_characters': telegram_scraper.min_characters,
            'reverse': telegram_scraper.reverse
        })
        await set_telegram_scraper_task_id(
            object_id=telegram_scraper.id,
            task_id=task_result.id
        )

    telegram_updates_scraper_conf = await get_telegram_updates_scraper_conf()
    if telegram_updates_scraper_conf.task_id:
        celery.control.revoke(
            telegram_updates_scraper_conf.task_id,
            terminate=True
        )

    task_result = listen_for_new_telegram_channel_messages_task.apply_async(kwargs={
        'channel_link_list': [i.channel_link for i in telegram_scraper_list]
    })
    await set_telegram_updates_scraper_task_id(
        task_id=task_result.id
    )
