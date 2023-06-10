from celery import Celery
from pydantic import HttpUrl
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from asgiref.sync import async_to_sync

from .config import (
    logger,
    MTPROTO_TOKEN,
    MTPROTO_API_ID,
    MTPROTO_API_HASH,
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND
)
from .database import init_db
from .telegram_scraper.documents import TelegramScraper
from .telegram_scraper.utils import scrape_message_async
from .telegram_scraper.services import (
    get_telegram_scraper_by_channel_link,
    get_telegram_scraper_list,
    set_telegram_scraper_job_id,
    increment_telegram_scraper_offset,
    add_adding_statistic_item
)
from .telegram_updates_scraper_conf.services import (
    get_telegram_updates_scraper_conf,
    set_telegram_updates_scraper_job_id
)


celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


async def scrape_telegram_channel_job(
    channel_link: HttpUrl,
    offset: int = 0,
    limit: int | None = None,
    min_characters: int = 280,
    reverse: bool = False
) -> bool:
    logger.info(f'start scrape for {channel_link=} {offset=} {limit=}')

    await init_db()
    client = TelegramClient(
        session=StringSession(MTPROTO_TOKEN),
        api_id=MTPROTO_API_ID,
        api_hash=MTPROTO_API_HASH
    )
    await client.start()
    client.parse_mode = 'html'

    channel = await client.get_entity(channel_link)
    async for message in client.iter_messages(
        entity=channel,
        add_offset=offset,
        limit=limit,
        reverse=reverse
    ):
        telegram_scraper = await get_telegram_scraper_by_channel_link(channel_link)
        while not telegram_scraper.is_running:
            telegram_scraper = await get_telegram_scraper_by_channel_link(channel_link)

        await increment_telegram_scraper_offset(telegram_scraper.id)
        article_added_successfully = await scrape_message_async(
            min_characters=min_characters,
            message=message,
            channel=channel
        )
        if article_added_successfully:
            logger.info('add new statistic item')
            await add_adding_statistic_item(telegram_scraper.id)
    return True


@celery.task
def scrape_telegram_channel_job_wrapper(
    channel_link: HttpUrl,
    offset: int = 0,
    limit: int | None = None,
    min_characters: int = 280,
    reverse: bool = False
) -> bool:
    async_to_sync(scrape_telegram_channel_job)(
        channel_link=channel_link,
        offset=offset,
        limit=limit,
        min_characters=min_characters,
        reverse=reverse
    )


async def listen_for_new_telegram_channel_messages_job(channel_link_list: list[HttpUrl]):
    async with TelegramClient(
        session=StringSession(MTPROTO_TOKEN),
        api_id=MTPROTO_API_ID,
        api_hash=MTPROTO_API_HASH
    ) as client:
        client.parse_mode = 'html'

        @client.on(events.NewMessage(chats=channel_link_list))
        async def new_message_listener(event):
            await init_db()
            logger.info('start scraping new message')
            message = event.message
            channel = await event.get_chat()

            logger.debug(f'channel username {channel.username}')
            telegram_scraper = await get_telegram_scraper_by_channel_link(f'https://t.me/{channel.username}')
            min_characters = telegram_scraper.min_characters

            article_added_successfully = await scrape_message_async(
                min_characters=min_characters,
                message=message,
                channel=channel
            )
            if article_added_successfully:
                logger.info('add new statistic item')
                await add_adding_statistic_item(telegram_scraper.id)

        await client.run_until_disconnected()


@celery.task
def listen_for_new_telegram_channel_messages_job_wrapper(channel_link_list: list[HttpUrl]):
    async_to_sync(listen_for_new_telegram_channel_messages_job)(channel_link_list)


async def run_all_telegram_scrapers():
    telegram_scraper_list = await get_telegram_scraper_list()

    await run_linear_telegram_scrapers(telegram_scraper_list)
    await run_telegram_updates_scraper(telegram_scraper_list)


async def run_linear_telegram_scrapers(telegram_scraper_list: list[TelegramScraper]):
    for telegram_scraper in telegram_scraper_list:
        if telegram_scraper.job_id:
            celery.control.revoke(telegram_scraper.job_id, terminate=True)

        job = scrape_telegram_channel_job_wrapper.apply_async(kwargs=dict(
            channel_link=telegram_scraper.channel_link,
            offset=telegram_scraper.offset,
            limit=telegram_scraper.limit,
            min_characters=telegram_scraper.min_characters,
            reverse=telegram_scraper.reverse
        ))
        await set_telegram_scraper_job_id(
            object_id=telegram_scraper.id,
            job_id=job.id
        )


async def run_telegram_updates_scraper(telegram_scraper_list: list[TelegramScraper]):
    channel_link_list = [i.channel_link for i in telegram_scraper_list]
    telegram_updates_scraper_conf = await get_telegram_updates_scraper_conf()

    if telegram_updates_scraper_conf.job_id:
        celery.control.revoke(telegram_updates_scraper_conf.job_id, terminate=True)

    job = listen_for_new_telegram_channel_messages_job_wrapper.apply_async(kwargs=dict(
        channel_link_list=channel_link_list
    ))
    await set_telegram_updates_scraper_job_id(job.id)
