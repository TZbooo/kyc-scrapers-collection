from beanie import Document

from .base_config import ConfiguredBaseModel


class TelegramUpdatesScraperConf(Document, ConfiguredBaseModel):
    task_id: str | None = None
