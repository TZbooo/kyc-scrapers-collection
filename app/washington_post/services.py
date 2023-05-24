import io
import uuid
from datetime import datetime

import requests
from selenium import webdriver

from app.kyc import add_kyc_article


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
        article_item['additional_properties']['publish_date'][:-1]
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
        origin='https://www.washingtonpost.com/',
        source=article_url
    )

    print(f'''
    {article_url=}
    {date=}
    {title=}
    {image_url=}
    {html_text=}
    ''')


def get_washington_post_articles(driver: webdriver.Chrome, offset: int, limit: int) -> dict:
    return driver.execute_script(f'''
    return await (await fetch("https://www.washingtonpost.com/prism/api/prism-query?_website=washpost&query=%7B%22query%22%3A%22prism%3A%2F%2Fprism.query%2Fsite-articles-only%2C%2Fworld%2F%26offset%3D{offset}%26limit%3D{limit}%22%7D", {{
        "referrer": "https://www.washingtonpost.com/world/?itid=nb_world",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "method": "GET",
        "mode": "cors",
        "credentials": "include"
    }})).json();
    ''')
