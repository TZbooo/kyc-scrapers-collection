import itertools

from scraper.config import SCRAPING_CONF
from scraper.worker import celery
from .services import get_article_url_list, scrape_article_page


@celery.task(name='scrape_themoscowpost_task')
def scrape_themoscowpost_task() -> bool:
    for page in itertools.count(SCRAPING_CONF['themoscowtimes']['start_page']):
        article_url_list = get_article_url_list(page=page)

        for url in article_url_list:
            scrape_article_page(url)
        else:
            break
