import io
import uuid
import pytz
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from website_scrapers.config import logger
from website_scrapers.kyc import add_kyc_article
from website_scrapers.bsslib import get_driver, convert_article_parts_to_html


def get_article_image(driver: webdriver.Chrome) -> io.BytesIO | None:
    try:
        image_url = driver.find_element(
            By.CSS_SELECTOR, 'h2 + div img'
        ).get_attribute('src')
        driver.get(image_url)

        image = io.BytesIO(driver.find_element(
            By.CSS_SELECTOR, 'img[src^=http]'
        ).screenshot_as_png)
        image.name = f'moscow-post-{uuid.uuid4().hex}.png'
        return image
    except:
        return None


def get_article_url_list(driver: webdriver.Chrome, page: int, reverse: bool = True, limit: int | None = None) -> list[str]:
    sort_type = 'ASC' if reverse else 'DESC'
    now_msk = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%d.%m.%Y')
    logger.debug(f'current date in moscow {now_msk}')

    response = driver.execute_script(f'''
    return await (await fetch("http://www.moscow-post.su/all/?load=1&page={page}&start=1.01.2007&end={now_msk}&sort={sort_type}", {{
        "headers": {{
            "accept": "*/*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
        }},
        "referrer": "http://www.moscow-post.su/all/?load=1&page={page}&start=1.01.2007&end={now_msk}&sort={sort_type}",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": null,
        "method": "GET",
        "mode": "cors",
        "credentials": "include"
    }})).json();
    ''')
    article_url_list = [
        'http://www.moscow-post.su' + article_item['full_url']
        for article_item in response['articles'][:limit]
    ]
    logger.debug(article_url_list)

    return article_url_list


def scrape_article_page(driver: webdriver.Chrome, url: str):
    driver.get(url)
    logger.info('page was loaded')

    published_time_string = driver.find_element(
        By.CSS_SELECTOR,
        'meta[property="article:published_time"]'
    ).get_attribute('content')[5:][:-15]
    date = datetime.strptime(
        published_time_string,
        '%d %b %Y'
    ).strftime('%Y-%m-%d')

    title = driver.find_element(By.TAG_NAME, 'h1').text
    logger.debug(f'{title=} {url=}')

    try:
        sub_title = driver.find_element(By.TAG_NAME, 'h2').text
    except NoSuchElementException:
        sub_title = None

    text = driver.find_element(By.CLASS_NAME, 'article-text').text
    html_text = convert_article_parts_to_html(
        title=title,
        sub_title=sub_title,
        text=text
    )
    image = get_article_image(driver)

    add_kyc_article(
        name=title,
        description=html_text,
        date=date,
        image=image,
        origin='http://www.moscow-post.su/',
        source=url
    )


def scrape_moscow_post_articles_chunk(article_url_list: list[str]):
    driver = get_driver()
    try:
        for article_url in article_url_list:
            logger.info(f'start scraping {article_url}')
            scrape_article_page(
                driver=driver,
                url=article_url
            )
    finally:
        driver.quit()
