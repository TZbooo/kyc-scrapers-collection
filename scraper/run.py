from scraper.config import logger, SCRAPING_CONF
from scraper.moscow_post.tasks import scrape_moscow_post_task
from scraper.washington_post.tasks import scrape_washington_post_task
from scraper.lenta_ru.tasks import scrape_lenta_ru_task
from scraper.telegram_channel.tasks import scrape_telegram_channel_task, listen_for_new_channels_messages


def start_telegram_channels_scraping() -> list:
    return [
        scrape_telegram_channel_task.apply_async(
            kwargs={
                'channel_link': scraper['channel_link'],
                'offset': scraper['offset'],
                'limit': scraper['limit'],
                'reverse': scraper['reverse'],
                'min_characters': scraper['min_characters']
            },
            queue='regular'
        ) for scraper in SCRAPING_CONF['telegram']
    ]


def run_scraping_tasks():
    scraping_tasks = start_telegram_channels_scraping()

    while not all(task.ready() for task in scraping_tasks):
        continue

    logger.success('manual scraping complete! start listen for new messages')

    channel_username_list = [scraper['channel_link'] for scraper in SCRAPING_CONF['telegram']]
    logger.info(channel_username_list)

    listen_for_new_channels_messages.apply_async(
        kwargs={
            'channel_username_list': channel_username_list
        },
        queue='periodic'
    )

    if SCRAPING_CONF['moscow_post']['run_scraper']:
        logger.info('start moscow-post.su scraper')
        scrape_moscow_post_task.apply_async(queue='regular')
    if SCRAPING_CONF['lenta_ru']['run_scraper']:
        logger.info('start lenta.ru scraper')
        scrape_lenta_ru_task.apply_async(queue='regular')
    if SCRAPING_CONF['washington_post']['run_scraper']:
        logger.info('start washingtonpost.com scraper')
        scrape_washington_post_task.apply_async(queue='regular')


if __name__ == '__main__':
    run_scraping_tasks()