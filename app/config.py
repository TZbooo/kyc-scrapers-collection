import os
import json
import pathlib

from loguru import logger


logger.add('logs.log', serialize=True, rotation='1 day')

BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()

with open(BASE_DIR / 'scraping.json', 'r') as scraping_conf_file:
    SCRAPING_CONF = json.load(scraping_conf_file)

KYC_BASE_API_TOKEN = os.environ['KYC_BASE_API_TOKEN']

MTPROTO_TOKEN = os.environ['MTPROTO_TOKEN']
MTPROTO_API_HASH = os.environ['MTPROTO_API_HASH']
MTPROTO_API_ID = os.environ['MTPROTO_API_ID']

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']

MOSCOW_POST_COOKIES_LIST = [
    '__lhash_=0d9ba47f496fd35fd84064586b00b11c; _gid=GA1.2.1262841686.1684003182; tmr_lvid=6af5b28e0c6edfb9f0aff15ed8aa9417; tmr_lvidTS=1684003182108; adtech_uid=f2b68cde-d4c8-49bc-936e-77eb85962c6f%3Amoscow-post.su; top100_id=t1.7020705.844847242.1684003182386; _ym_uid=168400318499451436; _ym_d=1684003184; _ym_isad=2; uuid=624547d4c6cb34b9%3A1; __upin=RIgw7FJEmFkS/+CcXkuGZw; pmtimesig=[[1684003196055,0]]; __js_p_=10,1800,0,0,0; __jhash_=785; __jua_=Mozilla%2F5.0%20%28X11%3B%20Linux%20x86_64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F110.0.0.0%20Safari%2F537.36; __hash_=884f0a155b84cc46b753a6ae626c9719; _ym_visorc=b; _ga=GA1.2.152415158.1684003182; last_visit=1684006271708%3A%3A1684017071708; tmr_detect=0%7C1684017073955; _ga_K9NVDZQ134=GS1.1.1684017012.3.1.1684017153.0.0.0; t3_sid_7020705=s1.1109246196.1684017014332.1684017153833.3.14'
]
