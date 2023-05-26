import itertools

from scraper.config import logger, SCRAPING_CONF
from scraper.worker import celery
from .services import get_article_url_list, scrape_article_page


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        schedule=60 * 10,
        sig=check_for_new_themoscowtimes_articles_task.s().set(queue='periodic')
    )


@celery.task(name='check_for_new_themoscowtimes_articles_task')
def check_for_new_themoscowtimes_articles_task():
    article_url_list = get_article_url_list(page=0)
    logger.info(f'{article_url_list=}')

    for url in article_url_list:
        scrape_article_page(url)


@celery.task(name='scrape_themoscowpost_task')
def scrape_themoscowpost_task() -> bool:
    for page in itertools.count(SCRAPING_CONF['themoscowtimes']['start_page']):
        try:
            article_url_list = get_article_url_list(page=page)
            logger.info(f'{article_url_list=}')
            if not article_url_list:
                break

            for url in article_url_list:
                scrape_article_page(url)
        except Exception as e:
            logger.error(e)
    return True
