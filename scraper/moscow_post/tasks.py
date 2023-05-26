import time
import itertools
import pytz
from datetime import datetime

from selenium.common.exceptions import JavascriptException

from scraper.config import logger, SCRAPING_CONF
from scraper.worker import celery
from scraper.bsslib import get_driver
from .services import get_article_url_list, scrape_moscow_post_articles_chunk


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60 * 30, check_for_new_moscow_post_articles_task.s())


@celery.task(name='check_for_new_moscow_post_articles_task')
def check_for_new_moscow_post_articles_task() -> bool:
    driver = get_driver()
    try:
        driver.get('http://www.moscow-post.su/all/')
        logger.info('wait for page load')
        time.sleep(15)

        article_url_list = get_article_url_list(
            driver=driver,
            page=1,
            reverse=False,
            limit=2
        )
        scrape_moscow_post_articles_chunk(article_url_list)
        logger.info('new articles was checked')
    finally:
        driver.quit()
    return True


@celery.task(name='scrape_moscow_post_task')
def scrape_moscow_post_task() -> bool:
    now_msk = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y')
    logger.trace(f'current date in moscow {now_msk}')

    driver = get_driver()
    driver.get('http://www.moscow-post.su/all/')
    logger.info('wait for page load')
    time.sleep(15)

    for page in itertools.count(SCRAPING_CONF['moscow_post']['start_page']):
        logger.info(f'{page=}')

        if not page % 10:
            driver.quit()
            driver = get_driver()
            driver.get('http://www.moscow-post.su/all/')

            logger.info('wait for page load')
            time.sleep(15)
    
        try:
            article_url_list = get_article_url_list(
                driver=driver,
                reverse=SCRAPING_CONF['moscow_post']['reverse'],
                page=page
            )
        except JavascriptException:
            logger.error('scraper was detected')
            continue

        if not article_url_list:
            break

        scrape_moscow_post_articles_chunk(article_url_list)

    driver.quit()
    return True
