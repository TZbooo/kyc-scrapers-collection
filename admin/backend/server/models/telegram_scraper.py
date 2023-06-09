from pytz import timezone
from datetime import datetime

from beanie import Document
from pydantic import Field, BaseModel, HttpUrl

from .base_config import ConfiguredBaseModel


class ArticleAddingStatisticItem(BaseModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone('Europe/Moscow'))
    )


class TelegramScraper(Document, ConfiguredBaseModel):
    is_running: bool = False
    job_id: str | None = None

    article_adding_statistics: list[ArticleAddingStatisticItem] = []

    name: str
    channel_link: HttpUrl
    offset: int
    limit: int | None = None
    reverse: bool = True
    min_characters: int
