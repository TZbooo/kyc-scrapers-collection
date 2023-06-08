from beanie import PydanticObjectId
from pydantic import HttpUrl

from server.models.telegram_scraper import TelegramScraper


async def get_telegram_scraper_list(
    skip: int | None = None,
    limit: int | None = None
) -> list[TelegramScraper]:
    telegram_scraper_list = await TelegramScraper.all(
        skip=skip,
        limit=limit
    ).to_list()
    return telegram_scraper_list


async def get_telegram_scraper_by_channel_link(channel_link: HttpUrl) -> TelegramScraper:
    telegram_scraper = await TelegramScraper.find_one(
        TelegramScraper.channel_link == channel_link
    )
    return telegram_scraper


async def get_telegram_scraper_by_object_id(object_id: PydanticObjectId) -> TelegramScraper:
    telegram_scraper = await TelegramScraper.find_one(
        TelegramScraper.id == object_id
    )
    return telegram_scraper


async def add_telegram_scraper(
    channel_link: HttpUrl,
    offset: int,
    limit: int | None,
    reverse: bool,
    min_characters: int
) -> TelegramScraper:
    new_telegram_scraper = TelegramScraper(
        channel_link=channel_link,
        offset=offset,
        limit=limit,
        reverse=reverse,
        min_characters=min_characters
    )
    await new_telegram_scraper.create()
    return new_telegram_scraper


async def update_telegram_scraper(
    object_id: PydanticObjectId,
    channel_link: HttpUrl,
    offset: int,
    limit: int | None,
    reverse: bool,
    min_characters: int
) -> TelegramScraper:
    telegram_scraper = await get_telegram_scraper_by_object_id(object_id)

    await telegram_scraper.set({
        TelegramScraper.channel_link: channel_link,
        TelegramScraper.offset: offset,
        TelegramScraper.limit: limit,
        TelegramScraper.reverse: reverse,
        TelegramScraper.min_characters: min_characters
    })

    updated_telegram_scraper = await get_telegram_scraper_by_object_id(object_id)
    return updated_telegram_scraper


async def set_telegram_scraper_job_id(
    object_id: PydanticObjectId,
    job_id: str
) -> TelegramScraper:
    telegram_scraper = await get_telegram_scraper_by_object_id(object_id)
    await telegram_scraper.set({
        TelegramScraper.job_id: job_id
    })

    updated_telegram_scraper = await get_telegram_scraper_by_object_id(object_id)
    return updated_telegram_scraper


async def set_telegram_scraper_running_status(
    object_id: PydanticObjectId,
    running_status: bool
) -> TelegramScraper:
    telegram_scraper = await get_telegram_scraper_by_object_id(object_id)
    await telegram_scraper.set({
        TelegramScraper.is_running: running_status
    })

    updated_telegram_scraper = await get_telegram_scraper_by_object_id(object_id)
    return updated_telegram_scraper


async def increment_telegram_scraper_offset(object_id: PydanticObjectId) -> TelegramScraper:
    telegram_scraper = await get_telegram_scraper_by_object_id(object_id)
    await telegram_scraper.inc({
        TelegramScraper.offset: 1
    })

    updated_telegram_scraper = await get_telegram_scraper_by_object_id(object_id)
    return updated_telegram_scraper


async def delete_telegram_scraper(object_id: PydanticObjectId) -> bool:
    telegram_scraper = await get_telegram_scraper_by_object_id(object_id)
    await telegram_scraper.delete()
    return True
