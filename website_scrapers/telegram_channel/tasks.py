from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession

from website_scrapers.config import (
    logger,

    MTPROTO_TOKEN,
    MTPROTO_API_ID,
    MTPROTO_API_HASH
)
from website_scrapers.worker import celery
from .services import (
    scrape_message,
    scrape_message_async,
    get_scraper_conf_by_channel_username
)


@celery.task(name='scrape_telegram_channel_task')
def scrape_telegram_channel_task(
    channel_link: str,
    offset: int = 0,
    limit: int | None = None,
    min_characters: int = 280,
    reverse: bool = False
) -> bool:
    logger.info(f'start scrape for {channel_link=}')
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


@celery.task(name='listen_for_new_channels_messages')
def listen_for_new_channels_messages(channel_username_list: list[str]):
    with TelegramClient(StringSession(MTPROTO_TOKEN), MTPROTO_API_ID, MTPROTO_API_HASH) as client:
        client.parse_mode = 'html'

        @client.on(events.NewMessage(chats=channel_username_list))
        async def new_message_listener(event):
            logger.info('start scraping new message')
            message = event.message
            channel = await event.get_chat()

            logger.debug(f'channel username {channel.username}')
            scraper = get_scraper_conf_by_channel_username(channel.username)
            min_characters = scraper['min_characters']

            await scrape_message_async(
                min_characters=min_characters,
                message=message,
                channel=channel
            )

        client.run_until_disconnected()
