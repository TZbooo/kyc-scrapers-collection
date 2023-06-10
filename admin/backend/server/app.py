from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .telegram_updates_scraper_conf.services import add_telegram_updates_scraper_conf_if_not_exists
from .tasks import run_all_telegram_scrapers
from .telegram_scraper.routes import telegram_scraper_router


app = FastAPI()

app.include_router(telegram_scraper_router)

origins = [
    'http://localhost:8080',
    'http://45.153.35.218:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup():
    await init_db()

    await add_telegram_updates_scraper_conf_if_not_exists()
    await run_all_telegram_scrapers()
