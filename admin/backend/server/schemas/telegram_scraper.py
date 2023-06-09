from pytz import timezone
from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, HttpUrl, Field, validator

from server.models.telegram_scraper import ArticleAddingStatisticItem


class BaseTelegramScraperSchema(BaseModel):
    name: str
    is_running: bool
    channel_link: HttpUrl
    offset: int
    limit: int | None = None
    reverse: bool = True
    min_characters: int


class AddTelegramScraperSchema(BaseTelegramScraperSchema):
    pass


class UpdateTelegramScraperSchema(BaseTelegramScraperSchema):
    object_id: PydanticObjectId
    is_running: None = None


class UpdateTelegramScraperRunningStatusSchema(BaseModel):
    object_id: PydanticObjectId
    is_running: bool


class DeleteTelegramScraperSchema(BaseModel):
    object_id: PydanticObjectId


class GetTelegramScraperSchema(BaseTelegramScraperSchema):
    object_id: PydanticObjectId = Field(alias='_id')

    article_adding_statistics: list[ArticleAddingStatisticItem] = []
    total: int = None
    total_per_month: int = None
    total_per_day: int = None

    @validator('total', always=True)
    def compute_total(cls, total: int | None, values: dict | None) -> int:
        article_adding_statistics = values['article_adding_statistics']
        return len(article_adding_statistics)
    
    @validator('total_per_month', always=True)
    def compute_total_per_month(cls, total_per_month: int | None, values: dict | None) -> int:
        article_adding_statistics = values['article_adding_statistics']

        now_msk = datetime.now(timezone('Europe/Moscow'))
        total_per_month = 0
        for i in article_adding_statistics:
            if (i.created_at.year == now_msk.year) and (i.created_at.month == now_msk.month):
                total_per_month += 1
        return total_per_month

    @validator('total_per_day', always=True)
    def compute_total_per_day(value, values, config, field):
        article_adding_statistics = values['article_adding_statistics']

        now_msk = datetime.now(timezone('Europe/Moscow'))
        total_per_day = 0
        for i in article_adding_statistics:
            if (i.created_at.year == now_msk.year) and (i.created_at.month == now_msk.month) and (i.created_at.day == now_msk.day):
                total_per_day += 1
        return total_per_day
