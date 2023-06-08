from datetime import datetime

from beanie import Document
from pydantic import BaseModel, HttpUrl

from .base_config import ConfiguredBaseModel


class ArticleAddingStatisticItem(BaseModel):
    date: datetime


class TelegramScraper(Document, ConfiguredBaseModel):
    is_running: bool = False
    job_id: str | None = None

    article_adding_statistics: list[ArticleAddingStatisticItem] = []

    channel_link: HttpUrl
    offset: int
    limit: int | None = None
    reverse: bool = True
    min_characters: int
