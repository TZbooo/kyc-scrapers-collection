from pydantic import validate_arguments, HttpUrl

from server.models.telegram_scraper import TelegramScraper


@validate_arguments
async def get_telegram_scraper_list(
    skip: int | None = None,
    limit: int | None = None
) -> list[TelegramScraper]:
    telegram_scraper_list = await TelegramScraper.all(
        skip=skip,
        limit=limit
    ).to_list()
    return telegram_scraper_list


@validate_arguments
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
