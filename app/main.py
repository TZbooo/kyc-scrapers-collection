from itertools import count
from typing import Generator

from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession

from app.config import (
    logger,

    MTPROTO_TOKEN,
    MTPROTO_API_ID,
    MTPROTO_API_HASH,

    SCRAPING_CONF
)
from app.services import scrape_message, get_scraper_conf_by_channel_username
from app.worker import scrape_channel_task


def start_scraping() -> Generator:
    return [
        scrape_channel_task.apply_async(kwargs={
            'channel_link': scraper['channel_link'],
            'offset': scraper['offset'],
            'limit': scraper['limit'],
            'reverse': scraper['reverse'],
            'min_characters': scraper['min_characters']
        }) for scraper in SCRAPING_CONF
    ]


if __name__ == '__main__':
    scraping_tasks = start_scraping()

    for i in count(0):
        if all(task.ready() for task in scraping_tasks):
            logger.info('manual scraping complete! start listen for new messages')
            break

    channel_usernames_list = [scraper['channel_link'] for scraper in SCRAPING_CONF]
    logger.info(channel_usernames_list)
    with TelegramClient(StringSession(MTPROTO_TOKEN), MTPROTO_API_ID, MTPROTO_API_HASH) as client:
        client.parse_mode = 'html'

        @client.on(events.NewMessage(chats=channel_usernames_list))
        async def new_message_checker(event):
            logger.info('start scraping new message')
            message = event.message
            channel = await event.get_chat()
            
            scraper = get_scraper_conf_by_channel_username(channel.username)
            min_characters = scraper['min_characters']

            scrape_message(
                min_characters=min_characters,
                message=message,
                channel=channel
            )

        client.run_until_disconnected()