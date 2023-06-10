from website_scrapers.config import logger, SCRAPING_CONF
from website_scrapers.moscow_post.tasks import scrape_moscow_post_task
from website_scrapers.washington_post.tasks import scrape_washington_post_task
from website_scrapers.themoscowtimes.tasks import scrape_themoscowpost_task
from website_scrapers.lenta_ru.tasks import scrape_lenta_ru_task
from website_scrapers.compromat.tasks import scrape_compromat_task


def run_scraping_tasks():
    if SCRAPING_CONF['moscow_post']['run_scraper']:
        logger.info('start moscow-post.su scraper')
        scrape_moscow_post_task.apply_async()
    if SCRAPING_CONF['lenta_ru']['run_scraper']:
        logger.info('start lenta.ru scraper')
        scrape_lenta_ru_task.apply_async()
    if SCRAPING_CONF['washington_post']['run_scraper']:
        logger.info('start washingtonpost.com scraper')
        scrape_washington_post_task.apply_async()
    if SCRAPING_CONF['themoscowtimes']['run_scraper']:
        logger.info('start themoscowtimes.com scraper')
        scrape_themoscowpost_task.apply_async()
    if SCRAPING_CONF['compromat']['run_scraper']:
        logger.info('start compromat.ru scraper')
        scrape_compromat_task.apply_async()


if __name__ == '__main__':
    run_scraping_tasks()
