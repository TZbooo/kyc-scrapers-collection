from server.models.telegram_updates_scraper_conf import TelegramUpdatesScraperConf


async def get_telegram_updates_scraper_conf() -> TelegramUpdatesScraperConf | None:
    telegram_updates_scraper_conf = await TelegramUpdatesScraperConf.all().first_or_none()
    return telegram_updates_scraper_conf


async def add_telegram_updates_scraper_conf_if_not_exists():
    telegram_updates_scraper_conf_list = await get_telegram_updates_scraper_conf()

    if not telegram_updates_scraper_conf_list:
        new_telegram_updates_scraper_conf = TelegramUpdatesScraperConf()
        await new_telegram_updates_scraper_conf.create()


async def set_telegram_updates_scraper_job_id(job_id: str) -> TelegramUpdatesScraperConf:
    telegram_updates_scraper = await get_telegram_updates_scraper_conf()
    await telegram_updates_scraper.set({
        TelegramUpdatesScraperConf.job_id: job_id
    })

    updated_telegram_updates_scraper = await get_telegram_updates_scraper_conf()
    return updated_telegram_updates_scraper
