import time
import pytz
import itertools
from datetime import datetime, timedelta

from app.config import SCRAPING_CONF
from app.worker import celery
from .services import (
    get_article_url_list,
    scrape_lenta_ru_articles_chunk
)


@celery.task(name='check_for_new_lenta_ru_articles_task')
def check_for_new_lenta_ru_articles_task() -> bool:
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
        day=lenta_ru_conf['day']
    )
    for days in itertools.count(0):
        print(f'{days=}')
        try:
            scraping_date = start_scraping_date + timedelta(days=days)
            archive_url_template = 'https://lenta.ru/' + scraping_date.strftime('%Y/%m/%d') + '/page/{page}/'
            article_url_list = get_article_url_list(archive_url_template)
            scrape_lenta_ru_articles_chunk(article_url_list)
        except Exception as e:
            print(f'error {e}')
    return True
