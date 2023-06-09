from beanie import PydanticObjectId
from pydantic import BaseModel, HttpUrl, Field
from bson import ObjectId


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
