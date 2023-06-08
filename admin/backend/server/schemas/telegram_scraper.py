from beanie import PydanticObjectId
from pydantic import BaseModel, HttpUrl


class BaseTelegramScraperSchema(BaseModel):
    channel_link: HttpUrl
    offset: int
    limit: int | None = None
    reverse: bool = True
    min_characters: int


class AddTelegramScraperSchema(BaseTelegramScraperSchema):
    pass


class UpdateTelegramScraperSchema(BaseTelegramScraperSchema):
    object_id: PydanticObjectId


class UpdateTelegramScraperRunningStatusSchema(BaseModel):
    object_id: PydanticObjectId
    running_status: bool


class DeleteTelegramScraperSchema(BaseModel):
    object_id: PydanticObjectId


class GetTelegramScraperSchema(BaseTelegramScraperSchema):
    is_running: bool
