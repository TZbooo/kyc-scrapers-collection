import time
import itertools

from scraper.config import logger, SCRAPING_CONF
from scraper.worker import celery
from .services import Localization, get_article_url_list, scrape_article_page


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        schedule=60 * 10,
        sig=check_for_new_themoscowtimes_articles_task.s().set(queue='periodic')
    )


@celery.task(name='check_for_new_themoscowtimes_articles_task')
def check_for_new_themoscowtimes_articles_task():
    ru_article_url_list = get_article_url_list(
        page=0,
        localization=Localization.ru
    )
    en_article_url_list = get_article_url_list(
        page=0,
        localization=Localization.en
    )
    logger.info(f'{ru_article_url_list=} {en_article_url_list}')

    for url in ru_article_url_list:
        scrape_article_page(url)
    for url in en_article_url_list:
        scrape_article_page(url)


@celery.task(name='scrape_themoscowpost_task')
def scrape_themoscowpost_task() -> bool:
    for page in itertools.count(SCRAPING_CONF['themoscowtimes']['start_page']):
        try:
            ru_article_url_list = get_article_url_list(
                page=page,
                localization=Localization.ru
            )
            en_article_url_list = get_article_url_list(
                page=page,
                localization=Localization.en
            )
            logger.info(f'{ru_article_url_list=} {en_article_url_list}')
            if not (ru_article_url_list or en_article_url_list):
                break

            for url in ru_article_url_list:
                scrape_article_page(url)
            for url in en_article_url_list:
                scrape_article_page(url)

            time.sleep(2)
        except Exception as e:
            logger.error(e)
    return True
