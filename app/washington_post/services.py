import io
import uuid
import enum
from datetime import datetime

import requests
from selenium import webdriver

from app.config import logger
from app.kyc import add_kyc_article
from app.bsslib import get_driver


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
{html_text=}
    ''')


def scrape_all_artciles_from_category(
    articles_count: int,
    category: ArticleCategories,
    limit: int | None = None
):
    driver = get_driver()
    driver.get(f'https://www.washingtonpost.com/{category.name}/?itid=nb_{category.name}')

    for i, offset in enumerate(range(0, articles_count + 20, 20)):
        if i == limit:
            break

        logger.debug(f'offset={offset} limit={offset + 20}')
        articles = get_washington_post_articles(
            driver=driver,
            category=category,
            offset=offset,
            limit=offset + 20
        )

        for article_item in articles['items']:
            scrape_article_item(article_item)
        
        if i % 40:
            driver = get_driver()
            driver.get(f'https://www.washingtonpost.com/{category.name}/?itid=nb_{category.name}')



def get_washington_post_articles(
    driver: webdriver.Chrome,
    category: ArticleCategories,
    offset: int,
    limit: int
) -> dict:
    if category.name != 'investigations':
        return driver.execute_script(f'''
        return await (await fetch("https://www.washingtonpost.com/prism/api/prism-query?_website=washpost&query=%7B%22query%22%3A%22prism%3A%2F%2Fprism.query%2Fsite-articles-only%2C%2F{category.name}%2F%26offset%3D{offset}%26limit%3D{limit}%22%7D", {{
            "referrer": "https://www.washingtonpost.com/{category.name}/?itid=nb_{category.name}",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "mode": "cors",
            "credentials": "include"
        }})).json();
        ''')
    return driver.execute_script(f'''
    return await (await fetch("https://www.washingtonpost.com/prism/api/prism-query?_website=washpost&query=%7B%22query%22%3A%22prism%3A%2F%2Fprism.query%2Fsite%2C%2Fnational%2Finvestigations%26offset%3D{offset}%26limit%3D{limit}%22%7D", {{
        "referrer": "https://www.washingtonpost.com/national/investigations/?itid=nb_investigations",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "mode": "cors",
        "credentials": "include"
    }})).json();
    ''')
