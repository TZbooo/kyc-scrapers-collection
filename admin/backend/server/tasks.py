from pydantic import HttpUrl
from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from arq import ArqRedis, create_pool
from arq.jobs import Job
from arq.connections import RedisSettings

from .config import (
    logger,

    MTPROTO_TOKEN,
    MTPROTO_API_ID,
    MTPROTO_API_HASH
)
from .database import init_db
from .models.telegram_scraper import TelegramScraper
from .utils.telegram_scraper import scrape_message_async
from .services.telegram_scraper import (
    get_telegram_scraper_by_channel_link,
    get_telegram_scraper_list,
    set_telegram_scraper_job_id,
    increment_telegram_scraper_offset,
    add_adding_statistic_item
)
from .services.telegram_updates_scraper_conf import (
    get_telegram_updates_scraper_conf,
    set_telegram_updates_scraper_job_id
)


async def scrape_telegram_channel_job(
    ctx,
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


async def listen_for_new_telegram_channel_messages_job(ctx, channel_link_list: list[HttpUrl]):
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


async def run_all_telegram_scrapers():
    pool = await create_pool(RedisSettings(host='redis'))
    telegram_scraper_list = await get_telegram_scraper_list()

    await run_linear_telegram_scrapers(
        pool=pool,
        telegram_scraper_list=telegram_scraper_list
    )
    await run_telegram_updates_scraper(
        pool=pool,
        telegram_scraper_list=telegram_scraper_list
    )


async def run_linear_telegram_scrapers(
    pool: ArqRedis,
    telegram_scraper_list: list[TelegramScraper]
):
    for telegram_scraper in telegram_scraper_list:
        job = Job(telegram_scraper.job_id, pool)
        try:
            await job.abort()
            logger.success(f'success abort job {telegram_scraper.job_id}')
        except Exception as e:
            logger.error(f'cannot abort job: {e}')

        job = await pool.enqueue_job(
            'scrape_telegram_channel_job',
            channel_link=telegram_scraper.channel_link,
            offset=telegram_scraper.offset,
            limit=telegram_scraper.limit,
            min_characters=telegram_scraper.min_characters,
            reverse=telegram_scraper.reverse
        )
        await set_telegram_scraper_job_id(
            object_id=telegram_scraper.id,
            job_id=job.job_id
        )


async def run_telegram_updates_scraper(
    pool: ArqRedis,
    telegram_scraper_list: list[TelegramScraper]
):
    channel_link_list = [i.channel_link for i in telegram_scraper_list]
    telegram_updates_scraper_conf = await get_telegram_updates_scraper_conf()
    job = Job(telegram_updates_scraper_conf.job_id, pool)
    try:
        await job.abort()
        logger.success(
            f'success abort job {telegram_updates_scraper_conf.job_id}'
        )
    except Exception as e:
        logger.error(f'cannot abort job: {e}')

    job = await pool.enqueue_job(
        'listen_for_new_telegram_channel_messages_job',
        channel_link_list=channel_link_list
    )
    await set_telegram_updates_scraper_job_id(job.job_id)
