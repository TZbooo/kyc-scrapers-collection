from celery import Celery

from .config import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND
)


celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND
