import time

from scraper.config import logger, SCRAPING_CONF
from scraper.worker import celery
from scraper.bsslib import get_driver
from .services import (
    ArticleCategories,
    get_washington_post_articles,
    scrape_all_artciles_from_category
)


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        schedule=60 * 30,
        sig=check_for_new_washington_post_articles_task.s().set(queue='periodic')
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
    categories_settings = SCRAPING_CONF['washington_post']['categories_settings']
    driver = get_driver()

    for category in ArticleCategories:
        logger.info(f'start scraping {category.name} category')
        if categories_settings[category.name]['skip']:
            logger.info(f'category {category.name} skip')
            continue

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
            offset=categories_settings[category.name]['offset']
        )
    return True