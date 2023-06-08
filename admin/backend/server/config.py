import os

from loguru import logger
from redis import Redis


logger.add('logs/log_{time}.log', rotation='1 week', compression='zip')

redis = Redis(host='redis', port=6379, db=0)

KYC_BASE_API_TOKEN = os.environ['KYC_BASE_API_TOKEN']

MONGO_URL = os.environ['ME_CONFIG_MONGODB_URL']

MTPROTO_TOKEN = os.environ['MTPROTO_TOKEN']
MTPROTO_API_HASH = os.environ['MTPROTO_API_HASH']
MTPROTO_API_ID = os.environ['MTPROTO_API_ID']
