from pydantic import BaseModel, HttpUrl


class BaseTelegramScraperSchema(BaseModel):
    channel_link: HttpUrl
    offset: int
    limit: int | None = None
    reverse: bool = True
    min_characters: int


class AddTelegramScraperSchema(BaseTelegramScraperSchema):
    pass


class GetTelegramScraperSchema(BaseTelegramScraperSchema):
    is_running: bool
