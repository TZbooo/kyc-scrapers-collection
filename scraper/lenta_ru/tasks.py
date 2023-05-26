import time
import pytz
from datetime import datetime, timedelta

from scraper.config import SCRAPING_CONF
from scraper.worker import celery
from .services import (
    get_article_url_list,
    scrape_lenta_ru_articles_chunk
)


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic(
        schedule=60 * 20,
        sig=check_for_new_lenta_ru_articles_task.s().set(queue='periodic')
    )


@celery.task(name='check_for_new_lenta_ru_articles_task')
def check_for_new_lenta_ru_articles_task():
    while True:
        now_msk = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y/%m/%d')
        archive_page_url_template = 'https://lenta.ru/' + now_msk + '/page/{page}/'
        article_url_list = get_article_url_list(archive_page_url_template, limit=1)
        scrape_lenta_ru_articles_chunk(article_url_list)
        time.sleep(60 * 20)


@celery.task(name='scrape_lenta_ru_task')
def scrape_lenta_ru_task() -> bool:
    lenta_ru_conf = SCRAPING_CONF['lenta_ru']

    start_scraping_date = datetime(
        year=lenta_ru_conf['year'],
        month=lenta_ru_conf['month'],
        day=lenta_ru_conf['day'],
        tzinfo=pytz.timezone('Europe/Moscow')
    )
    now_msk = datetime.now(pytz.timezone('Europe/Moscow'))
    days = (now_msk - start_scraping_date).days

    for day in range(days):
        print(f'{day=}')
        try:
            scraping_date = start_scraping_date + timedelta(days=day)
            archive_url_template = 'https://lenta.ru/' + scraping_date.strftime('%Y/%m/%d') + '/page/{page}/'
            article_url_list = get_article_url_list(archive_url_template)
            scrape_lenta_ru_articles_chunk(article_url_list)
        except Exception as e:
            print(f'error {e}')
    return True
