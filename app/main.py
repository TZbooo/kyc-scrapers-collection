from typing import Generator

from app.config import logger, SCRAPING_CONF
from app.telegram_channel.tasks import scrape_telegram_channel_task, listen_for_new_channels_messages


def start_telegram_channels_scraping() -> Generator:
    return [
        scrape_telegram_channel_task.apply_async(kwargs={
            'channel_link': scraper['channel_link'],
            'offset': scraper['offset'],
            'limit': scraper['limit'],
            'reverse': scraper['reverse'],
            'min_characters': scraper['min_characters']
        }) for scraper in SCRAPING_CONF
    ]


if __name__ == '__main__':
    scraping_tasks = start_telegram_channels_scraping()

    while not all(task.ready() for task in scraping_tasks):
        continue

    logger.success('manual scraping complete! start listen for new messages')

    channel_username_list = [scraper['channel_link'] for scraper in SCRAPING_CONF]
    logger.info(channel_username_list)

    listen_for_new_channels_messages.apply_async(kwargs={'channel_username_list': channel_username_list})