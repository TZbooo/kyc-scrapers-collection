from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from .config import MONGO_URL

from .models.telegram_scraper import TelegramScraper
from .models.telegram_updates_scraper_conf import TelegramUpdatesScraperConf


async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client.kyc_scraper,
        document_models=[TelegramScraper, TelegramUpdatesScraperConf]
    )
