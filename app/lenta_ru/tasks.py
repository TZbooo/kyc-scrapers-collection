import itertools
from datetime import datetime, timedelta

from app.worker import celery
from .services import get_article_url_list, scrape_article_page
from bsslib import get_driver


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


@celery.task(name='scrape_lenta_ru_task')
def scrape_lenta_ru_task():
    start_scraping_date = datetime(year=2018, month=5, day=1)
    for days in itertools.count(0):
        scraping_date = start_scraping_date + timedelta(days=days)
        archive_url_template = 'https://lenta.ru/' + scraping_date.strftime('%Y/%m/%d') + '/page/{page}/'
        article_url_list = get_article_url_list(archive_url_template)
        scrape_lenta_ru_articles_chunk_task.apply_async(kwargs={
            'article_url_list': article_url_list
        })
        break
