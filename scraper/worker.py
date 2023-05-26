from celery import Celery

from scraper.config import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND
)


celery = Celery(__name__)
celery.control.purge()
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND
celery.autodiscover_tasks([
    'scraper.telegram_channel',
    'scraper.moscow_post',
    'scraper.lenta_ru',
    'scraper.washington_post',
    'scraper.themoscowtimes'
])
