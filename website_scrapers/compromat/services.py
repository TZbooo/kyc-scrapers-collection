import io
import uuid
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Comment
from pydantic import BaseModel, HttpUrl

from website_scrapers.config import logger
from website_scrapers.kyc import add_kyc_article
from . import WEBSITE_BASE_URL


class DatedArticle(BaseModel):
    url: HttpUrl
    date: str


def convert_article_parts_to_html_text(title: str, soup: BeautifulSoup) -> str:
    for a in soup.select('a'):
        if a.get('href') and not a['href'].startswith('http'):
            a['href'] = urljoin(WEBSITE_BASE_URL, a['href'])

    for comment in soup.find_all(text=lambda tag: isinstance(tag, Comment)):
        comment.extract()

    for figure in soup.select('figure'):
        figure.extract()

    html_text = f'<h1>{title}</h1>'
    for p in soup.select('.material_detail > h3 + h3 ~ p'):
        html_text += p.get_text()

    return html_text


def get_dated_article_list(month: int, year: int) -> list[str]:
    html = requests.get(
        f'https://www.compromat.ru/calendar_{month}_{year}.htm'
    ).text
    soup = BeautifulSoup(html, 'html.parser')

    for a, notice in zip(soup.select('.notices > a[href]'), soup.select('.notices')):
        url = urljoin(WEBSITE_BASE_URL, a['href'])
        date = datetime.strptime(
            notice.get_text().strip()[:10],
            '%d.%m.%Y'
        ).strftime('%Y-%m-%d')

        yield DatedArticle(
            url=url,
            date=date
        )


def scrape_article_page(url: str, date: str):
    html = requests.get(
        url
    ).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select_one('.material_detail > h3').text

    image_tag = soup.select_one('.material_detail img')
    image = None
    if image_tag:
        image_url = urljoin(WEBSITE_BASE_URL, image_tag['src'])
        image = io.BytesIO(requests.get(image_url).content)
        image.name = f'compromat-{uuid.uuid4().hex}.jpg'

    html_text = convert_article_parts_to_html_text(
        title=title,
        soup=soup
    )

    add_kyc_article(
        name=title,
        description=html_text,
        date=date,
        image=image,
        origin=WEBSITE_BASE_URL,
        source=url
    )
    logger.debug(f'{date=} {title=} {html_text=} {image=} {url=}')
