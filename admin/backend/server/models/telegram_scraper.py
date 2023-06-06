from uuid import UUID
from datetime import datetime

from beanie import Document, Indexed
from pydantic import BaseModel, HttpUrl


class ArticleAddingStatisticItem(BaseModel):
    date: datetime


class TelegramScraper(Document):
    is_running: bool = False
    task_id: Indexed(UUID, unique=True) | None = None

    article_adding_statistics: list[ArticleAddingStatisticItem] = []

    channel_link: HttpUrl
    offset: int
    limit: int | None = None
    reverse: bool = True
    min_characters: int


class TelegramUpdatesScraperConf(Document):
    task_id: Indexed(UUID, unique=True) | None = None
