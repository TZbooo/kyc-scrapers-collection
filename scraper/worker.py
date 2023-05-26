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
    'app.telegram_channel',
    'app.moscow_post',
    'app.lenta_ru',
    'app.washington_post'
])
