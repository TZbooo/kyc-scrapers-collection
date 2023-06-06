import pytz
from datetime import datetime
from website_scrapers.worker import celery

from dateutil.relativedelta import relativedelta

from website_scrapers.config import logger, SCRAPING_CONF
from .services import scrape_article_page, get_dated_article_list


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        schedule=60 * 20,
        sig=check_for_new_compromat_articles_task.s()
    )


@celery.task(name='check_for_new_compromat_articles_task')
def check_for_new_compromat_articles_task():
    now_msk = datetime.now(pytz.timezone('Europe/Moscow'))

    dated_article_list = get_dated_article_list(
        month=now_msk.month,
        year=now_msk.year
    )

    for dated_article in dated_article_list:
        try:
            scrape_article_page(
                url=dated_article.url,
                date=dated_article.date
            )
        except Exception as e:
            logger.error(e)


@celery.task(name='scrape_compromat_task')
def scrape_compromat_task():
    compromat_conf = SCRAPING_CONF['compromat']

    now_msk = datetime.now(pytz.timezone('Europe/Moscow'))
    latest_article_date = datetime(
        year=compromat_conf['year'],
        month=compromat_conf['month'],
        day=1
    )
    month_count = (now_msk.year - latest_article_date.year) \
        * 12 + (now_msk.month - latest_article_date.month)

    for month in range(month_count):
        current_date = latest_article_date + relativedelta(months=month)
        dated_article_list = get_dated_article_list(
            month=current_date.month,
            year=current_date.year
        )

        for dated_article in dated_article_list:
            try:
                scrape_article_page(
                    url=dated_article.url,
                    date=dated_article.date
                )
            except Exception as e:
                logger.error(e)
