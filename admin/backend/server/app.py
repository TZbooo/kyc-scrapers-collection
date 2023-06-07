from fastapi import FastAPI

from .database import init_db
from .schemas.telegram_scraper import (
    AddTelegramScraperSchema,
    UpdateTelegramScraperSchema,
    GetTelegramScraperSchema
)
from .services.telegram_scraper import (
    add_telegram_scraper,
    update_telegram_scraper,
    get_telegram_scraper_list
)
from .worker import scrape_telegram_channel_task


app = FastAPI()


@app.on_event('startup')
async def startup():
    await init_db()

    telegram_scraper_list = await get_telegram_scraper_list()
    for telegram_scraper in telegram_scraper_list:
        scrape_telegram_channel_task.apply_async(kwargs={
            'channel_link': telegram_scraper.channel_link,
            'offset': telegram_scraper.offset,
            'limit': telegram_scraper.limit,
            'min_characters': telegram_scraper.min_characters,
            'reverse': telegram_scraper.reverse
        })


@app.post('/')
async def add_telegram_scraper_post(data: AddTelegramScraperSchema) -> GetTelegramScraperSchema:
    new_telegram_scraper = await add_telegram_scraper(
        channel_link=data.channel_link,
        offset=data.offset,
        limit=data.limit,
        reverse=data.reverse,
        min_characters=data.min_characters
    )
    return new_telegram_scraper


@app.put('/')
async def update_telegram_scraper_put(data: UpdateTelegramScraperSchema) -> GetTelegramScraperSchema:
    updated_telegram_scraper = await update_telegram_scraper(
        object_id=data.object_id,
        channel_link=data.channel_link,
        offset=data.offset,
        limit=data.limit,
        reverse=data.reverse,
        min_characters=data.min_characters
    )
    return updated_telegram_scraper


@app.get('/')
async def get_telegram_scraper_list_get() -> list[GetTelegramScraperSchema]:
    telegram_scraper_list = await get_telegram_scraper_list()
    return telegram_scraper_list
