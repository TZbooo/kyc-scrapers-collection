from fastapi import FastAPI

from .database import init_db
from .schemas.telegram_scraper import (
    AddTelegramScraperSchema,
    GetTelegramScraperSchema
)
from . import services


app = FastAPI()


@app.on_event('startup')
async def startup():
    await init_db()


@app.post('/')
async def add_telegram_scraper(data: AddTelegramScraperSchema) -> GetTelegramScraperSchema:
    new_telegram_scraper = await services.add_telegram_scraper(
        channel_link=data.channel_link,
        offset=data.offset,
        limit=data.limit,
        reverse=data.reverse,
        min_characters=data.min_characters
    )
    return new_telegram_scraper


@app.get('/')
async def get_telegram_scraper_list() -> list[GetTelegramScraperSchema]:
    telegram_scraper_list = await services.get_telegram_scraper_list()
    return telegram_scraper_list
