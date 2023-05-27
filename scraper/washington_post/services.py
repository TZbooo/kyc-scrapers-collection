import time
import io
import uuid
import enum
from datetime import datetime

import requests

from scraper.config import logger
from scraper.kyc import add_kyc_article
from scraper.bsslib import get_driver


@enum.unique
class ArticleCategories(enum.Enum):
    world = 1
    politics = 2
    investigations = 3
    technology = 4
    lifestyle = 5


def convert_article_parts_to_html(title: str, article_parts: list[dict]) -> str:
    html_text = f'<h1>{title}</h1>'

    for element in article_parts:
        if element['type'] == 'text':
            content = element['content']
            html_text += f'<p>{content}</p>'
        if element['type'] == 'interstitial_link':
            content = element['content']
            url = element['url']
            html_text += f'<a href="{url}">{content}</a>'
        if element['type'] == 'header':
            content = element['content']
            level = element['level']
            html_text += f'<h{level}>{content}</h{level}>'
        if element['type'] == 'list':
            list_tag = 'ul' if element['list_type'] == 'unordered' else 'ol'

            html_text += f'<{list_tag}>'
            for li in element['items']:
                content = li['content']
                html_text += f'<li>{content}</li>'
            html_text += f'</{list_tag}>'
    
    return html_text


def scrape_article_item(article_item: dict):
    article_url = article_item['canonical_url']
    title = article_item['additional_properties']['page_title'].replace(' - The Washington Post', '')
    date = datetime.fromisoformat(
        article_item['created_date'][:-1]
    ).strftime('%Y-%m-%d')

    image = None
    if article_item['content_elements'][0]['type'] == 'image':
        image_url = article_item['content_elements'][0].get('url')
        image = io.BytesIO(requests.get(image_url).content)
        image.name = f'washington-post-{uuid.uuid4().hex}.jpg'

    html_text = convert_article_parts_to_html(
        title=title,
        article_parts=article_item['content_elements']
    )

    add_kyc_article(
        name=title,
        description=html_text,
        date=date,
        image=image,
        origin='https://www.washingtonpost.com/',
        source=article_url
    )

    logger.debug(f'''
{article_url=}
{date=}
{title=}
{image=}
    ''')


def scrape_all_artciles_from_category(
    articles_count: int,
    category: ArticleCategories,
    limit: int | None = None,
    offset: int = 0
):
    step = 20
    for i, offset in enumerate(range(offset, articles_count + step, step)):
        if i == limit:
            break

        logger.debug(f'{i=} offset={offset} limit={offset + step}')
        try:
            articles = get_washington_post_articles(
                category=category,
                offset=offset,
                limit=offset + step
            )
        except Exception as e:
            logger.error(e)
            continue

        for article_item in articles['items']:
            try:
                scrape_article_item(article_item)
            except Exception as e:
                logger.error(e)
        
        time.sleep(2)



def get_washington_post_articles(
    category: ArticleCategories,
    offset: int,
    limit: int
) -> dict:
    params = {
        '_website': 'washpost',
        'query': f'{{"query":"prism://prism.query/site-articles-only,/{category.name}&offset={offset}&limit={limit}"}}',
    }
    if category.name == 'investigations':
        params = {
            '_website': 'washpost',
            'query': f'{{"query":"prism://prism.query/site,/national/{category.name}&offset={offset}&limit={limit}"}}',
        }

    response = requests.get('https://www.washingtonpost.com/prism/api/prism-query', params=params)
    return response.json()