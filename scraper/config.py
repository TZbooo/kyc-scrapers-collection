import os
import json
import pathlib
import itertools

from loguru import logger


logger.add('log_{time}.log', rotation='1 week', compression='zip')

BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()

with open(BASE_DIR / 'scraping.json', 'r') as scraping_conf_file:
    SCRAPING_CONF = json.load(scraping_conf_file)

KYC_BASE_API_TOKEN = os.environ['KYC_BASE_API_TOKEN']

MTPROTO_TOKEN = os.environ['MTPROTO_TOKEN']
MTPROTO_API_HASH = os.environ['MTPROTO_API_HASH']
MTPROTO_API_ID = os.environ['MTPROTO_API_ID']

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']

BLOCK_BYPASS_PROXY = 'http://netbiom:golangvimo1qaz2wsx1AZ@185.213.208.247:3128'