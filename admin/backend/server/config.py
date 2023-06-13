import os
import itertools

from loguru import logger
from pydantic import BaseModel


logger.add('logs/log_{time}.log', rotation='1 week', compression='zip')


class MtprotoAccount(BaseModel):
    session: str
    api_id: int
    api_hash: str


KYC_BASE_API_TOKEN = os.environ['KYC_BASE_API_TOKEN']

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']

MONGO_URL = os.environ['ME_CONFIG_MONGODB_URL']

MTPROTO_ACCOUNT_CYCLE = itertools.cycle([
    MtprotoAccount(
        session='1ApWapzMBuxf8eU2fh53JQ7or0jiwoEM0MHc0ljPAEI9-tE6bf2R5nSbSIuvcgb0Z3hVxXUxvBnU-0WK-669pXAISuCcC28O1bu86ejh5UiEVaBsQEoSQhKv-tFYg0Y4eLy1w4NvYCvfjXVxlYf16TVyCvnCDEEqa7Uc18zMXY21xgAn74ZrSBVKopRpClxU2Cw8PaOj_4T8_-202C5zNMJG8B9ZKCD4IVtKU66I7F0U5ezNy_zsTL_yr71u0qA-C8jX7IkUqzgsa9ubprArt2mdqu7D27iWNvmcy4xuT0ZpspzV1Jd_Uok_A4GF8dSPM6GvFBkpdlAah_3EIgNVfHXzlRcphQPU=',
        api_id=10511894,
        api_hash='90a3c59c21a6c32256f2480bd43e778f'
    )
])
