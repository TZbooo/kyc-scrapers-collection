import os

from loguru import logger


logger.add('logs/log_{time}.log', rotation='1 week', compression='zip')

KYC_BASE_API_TOKEN = os.environ['KYC_BASE_API_TOKEN']

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']

MONGO_URL = os.environ['ME_CONFIG_MONGODB_URL']

MTPROTO_TOKEN = os.environ['MTPROTO_TOKEN']
MTPROTO_API_HASH = os.environ['MTPROTO_API_HASH']
MTPROTO_API_ID = os.environ['MTPROTO_API_ID']
