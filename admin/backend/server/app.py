from fastapi import FastAPI

from .database import init_db
from .schemas.telegram_scraper import (
    AddTelegramScraperSchema,
    UpdateTelegramScraperSchema,
    UpdateTelegramScraperRunningStatusSchema,
    DeleteTelegramScraperSchema,
    GetTelegramScraperSchema
)
from .services.telegram_scraper import (
    add_telegram_scraper,
    update_telegram_scraper,
    set_telegram_scraper_running_status,
    delete_telegram_scraper,
    get_telegram_scraper_list
)
from .services.telegram_updates_scraper_conf import add_telegram_updates_scraper_conf_if_not_exists
from .tasks import run_all_telegram_scrapers


app = FastAPI()


@app.on_event('startup')
async def startup():
    await init_db()

    await add_telegram_updates_scraper_conf_if_not_exists()
    await run_all_telegram_scrapers()


@app.post('/')
async def add_telegram_scraper_post(data: AddTelegramScraperSchema) -> GetTelegramScraperSchema:
    new_telegram_scraper = await add_telegram_scraper(
        channel_link=data.channel_link,
        offset=data.offset,
        limit=data.limit,
        reverse=data.reverse,
        min_characters=data.min_characters
    )
    await run_all_telegram_scrapers()
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
    await run_all_telegram_scrapers()
    return updated_telegram_scraper


@app.patch('/running_status')
async def set_telegram_scraper_running_status_patch(
    data: UpdateTelegramScraperRunningStatusSchema
) -> GetTelegramScraperSchema:
    updated_telegram_scraper = await set_telegram_scraper_running_status(
        object_id=data.object_id,
        running_status=data.running_status
    )
    return updated_telegram_scraper


@app.delete('/')
async def delete_telegram_scraper_delete(data: DeleteTelegramScraperSchema) -> bool:
    delete_telegram_scraper_status = await delete_telegram_scraper(object_id=data.object_id)
    await run_all_telegram_scrapers()
    return delete_telegram_scraper_status


@app.get('/')
async def get_telegram_scraper_list_get() -> list[GetTelegramScraperSchema]:
    telegram_scraper_list = await get_telegram_scraper_list()
    return telegram_scraper_list
