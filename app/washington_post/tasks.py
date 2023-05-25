import time

from app.config import logger
from app.worker import celery
from app.bsslib import get_driver
from .services import (
    ArticleCategories,
    get_washington_post_articles,
    scrape_all_artciles_from_category
)


@celery.task(name='check_for_new_washington_post_articles_task')
def check_for_new_washington_post_articles_task():
    while True:
        driver = get_driver()
        for category in ArticleCategories:
            logger.info(f'category={category.name}')
            driver.get(f'https://www.washingtonpost.com/{category.name}/?itid=nb_{category.name}')
            articles_count = get_washington_post_articles(
                driver=driver,
                category=category,
                offset=0,
                limit=1
            )['count']
            scrape_all_artciles_from_category(
                articles_count=articles_count,
                category=category,
                limit=1
            )
        time.sleep(60 * 20)


@celery.task(name='scrape_washington_post_task')
def scrape_washington_post_task() -> bool:
    driver = get_driver()

    for category in ArticleCategories:
        driver.get(f'https://www.washingtonpost.com/{category.name}/?itid=nb_{category.name}')
        articles_count = get_washington_post_articles(
            driver=driver,
            category=category,
            offset=0,
            limit=1
        )['count']
        scrape_all_artciles_from_category(
            articles_count=articles_count,
            category=category
        )
    return True
