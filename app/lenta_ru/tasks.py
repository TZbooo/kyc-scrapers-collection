import time
import pytz
import itertools
from datetime import datetime, timedelta

from app.worker import celery
from app.bsslib import get_driver
from .services import get_article_url_list, scrape_article_page


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60 * 20, check_for_new_lenta_ru_articles_task.s())


@celery.task(name='scrape_lenta_ru_articles_chunk_task')
def scrape_lenta_ru_articles_chunk_task(article_url_list: list[str]) -> bool:
    driver = get_driver()
    try:
        for article_url in article_url_list:
            scrape_article_page(
                driver=driver,
                url=article_url
            )
    finally:
        driver.quit()
    return True


@celery.task(name='check_for_new_lenta_ru_articles_task')
def check_for_new_lenta_ru_articles_task() -> bool:
    now_msk = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y/%m/%d')
    archive_page_url_template = 'https://lenta.ru/' + now_msk + '/page/{page}/'
    print(archive_page_url_template)
    article_url_list = get_article_url_list(archive_page_url_template, limit=1)
    scrape_lenta_ru_articles_chunk_task.apply_async(kwargs={
        'article_url_list': article_url_list
    })


@celery.task(name='scrape_lenta_ru_task')
def scrape_lenta_ru_task():
    start_scraping_date = datetime(year=2000, month=1, day=1)
    for days in itertools.count(0):
        scraping_date = start_scraping_date + timedelta(days=days)
        archive_url_template = 'https://lenta.ru/' + scraping_date.strftime('%Y/%m/%d') + '/page/{page}/'
        article_url_list = get_article_url_list(archive_url_template)
        scrape_lenta_ru_articles_chunk_task.apply_async(kwargs={
            'article_url_list': article_url_list
        })
        time.sleep(60)
