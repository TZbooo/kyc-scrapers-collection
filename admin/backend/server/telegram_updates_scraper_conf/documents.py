from beanie import Document


class TelegramUpdatesScraperConf(Document):
    job_id: str | None = None
