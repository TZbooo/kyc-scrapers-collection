from celery import Celery

from website_scrapers.config import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND
)


celery = Celery(__name__)
celery.control.purge()
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND
celery.autodiscover_tasks([
    'website_scrapers.moscow_post',
    'website_scrapers.lenta_ru',
    'website_scrapers.washington_post',
    'website_scrapers.themoscowtimes',
    'website_scrapers.compromat'
])
