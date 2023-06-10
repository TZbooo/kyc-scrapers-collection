from pytz import timezone
from datetime import datetime

from beanie import Document, Indexed
from pydantic import Field, BaseModel, HttpUrl


class ArticleAddingStatisticItem(BaseModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone('Europe/Moscow'))
    )


class TelegramScraper(Document):
    is_running: bool = False
    job_id: str | None = None

    article_adding_statistics: list[ArticleAddingStatisticItem] = []

    name: str
    channel_link: Indexed(HttpUrl, unique=True)
    offset: int
    limit: int | None = None
    reverse: bool = True
    min_characters: int
