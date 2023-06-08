from beanie import Document

from .base_config import ConfiguredBaseModel


class TelegramUpdatesScraperConf(Document, ConfiguredBaseModel):
    job_id: str | None = None
