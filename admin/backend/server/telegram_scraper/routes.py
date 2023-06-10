from fastapi import APIRouter

from .schemas import (
    AddTelegramScraperSchema,
    UpdateTelegramScraperSchema,
    UpdateTelegramScraperRunningStatusSchema,
    DeleteTelegramScraperSchema,
    GetTelegramScraperSchema
)
from .services import (
    add_telegram_scraper,
    update_telegram_scraper,
    set_telegram_scraper_running_status,
    delete_telegram_scraper,
    get_telegram_scraper_list
)
from server.jobs import run_all_telegram_scrapers


telegram_scraper_router = APIRouter()


@telegram_scraper_router.post('/', response_model_by_alias=False)
async def add_telegram_scraper_post(data: AddTelegramScraperSchema) -> GetTelegramScraperSchema:
    new_telegram_scraper = await add_telegram_scraper(
        name=data.name,
        is_running=data.is_running,
        channel_link=data.channel_link,
        offset=data.offset,
        limit=data.limit,
        reverse=data.reverse,
        min_characters=data.min_characters
    )
    await run_all_telegram_scrapers()
    return new_telegram_scraper


@telegram_scraper_router.put('/', response_model_by_alias=False)
async def update_telegram_scraper_put(data: UpdateTelegramScraperSchema) -> GetTelegramScraperSchema:
    updated_telegram_scraper = await update_telegram_scraper(
        object_id=data.object_id,
        name=data.name,
        channel_link=data.channel_link,
        offset=data.offset,
        limit=data.limit,
        reverse=data.reverse,
        min_characters=data.min_characters
    )
    await run_all_telegram_scrapers()
    return updated_telegram_scraper


@telegram_scraper_router.patch('/is_running', response_model_by_alias=False)
async def set_telegram_scraper_running_status_patch(
    data: UpdateTelegramScraperRunningStatusSchema
) -> GetTelegramScraperSchema:
    updated_telegram_scraper = await set_telegram_scraper_running_status(
        object_id=data.object_id,
        is_running=data.is_running
    )
    return updated_telegram_scraper


@telegram_scraper_router.delete('/')
async def delete_telegram_scraper_delete(data: DeleteTelegramScraperSchema) -> bool:
    delete_telegram_scraper_status = await delete_telegram_scraper(object_id=data.object_id)
    await run_all_telegram_scrapers()
    return delete_telegram_scraper_status


@telegram_scraper_router.get('/', response_model_by_alias=False)
async def get_telegram_scraper_list_get() -> list[GetTelegramScraperSchema]:
    telegram_scraper_list = await get_telegram_scraper_list()
    return telegram_scraper_list