import io
import enum
import uuid
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from website_scrapers.config import logger, BLOCK_BYPASS_PROXY
from website_scrapers.kyc import add_kyc_article


@enum.unique
class Localization(enum.Enum):
    en = 1
    ru = 2


proxies = {
    'https': BLOCK_BYPASS_PROXY
}


def convert_article_parts_to_html(title: str, soup: BeautifulSoup) -> str:
    html_text = f'<h1>{title}</h1>'
    article_block_list = soup.select_one(
        '.article__content .article__block--html'
    )

    for article_block in article_block_list:
        if not article_block.text.strip():
            continue
        html_text += str(article_block).strip()
    return html_text


def get_article_url_list(page: int, localization: Localization) -> list[str]:
    logger.info(f'start scraping page {page} articles')

    if localization.name == 'en':
        html = requests.get(
            f'https://www.themoscowtimes.com/news/{1 + 18 * page}',
            proxies=proxies
        ).text
        soup = BeautifulSoup(html, 'html.parser')
        return [article['data-url'] for article in soup.select('.article-excerpt-default')]

    if localization.name == 'ru':
        html = requests.get(
            f'https://www.moscowtimes.ru/news/{1 + 18 * page}'
        ).text
        soup = BeautifulSoup(html, 'html.parser')
        return [article['href'] for article in soup.select('.article-excerpt-default > a')]


def scrape_article_page(url: str):
    html = requests.get(url, proxies=proxies).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')[
        'content'].replace(' - The Moscow Times', '')
    date = datetime.fromisoformat(
        soup.select_one('meta[property="article:published_time"]')['content']
    ).strftime('%Y-%m-%d')

    image_url = soup.select_one('meta[property="og:image"]')['content']
    image = io.BytesIO(requests.get(image_url, proxies=proxies).content)
    image.name = f'themoscowtimes-{uuid.uuid4().hex}.jpg'

    html_text = convert_article_parts_to_html(
        title=title,
        soup=soup
    )

    logger.debug(f'{title=} {url=} {date=} {image=}')
    add_kyc_article(
        name=title,
        description=html_text,
        date=date,
        image=image,
        origin='https://www.themoscowtimes.com/',
        source=url
    )
