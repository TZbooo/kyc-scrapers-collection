import io
import uuid
import itertools

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from scraper.config import logger
from scraper.kyc import add_kyc_article
from scraper.bsslib import get_driver, convert_article_parts_to_html


def get_article_image(driver: webdriver.Chrome) -> io.BytesIO | None:
    try:
        image_url = driver.find_element(
            by=By.CLASS_NAME,
            value='picture__image'
        ).get_attribute('src')
        logger.debug(f'{image_url=}')

        response = requests.get(image_url)
        if not response.ok:
            return None

        image = io.BytesIO(response.content)
        image.name = f'lenta-ru-{uuid.uuid4().hex}.jpg'
        return image
    except:
        return None


def get_article_url_list(archive_page_url_template: str, limit: int | None = None) -> list[str]:
    driver = get_driver()

    article_url_list = []
    for page in itertools.count(1):
        page_url = archive_page_url_template.format(page=page)
        driver.get(page_url)
        logger.debug(page_url)

        page_article_url_list = [
            i.get_attribute('href')
            for i in driver.find_elements(By.CSS_SELECTOR, '.archive-page__item._news a')
        ]
        if not page_article_url_list:
            break
        article_url_list += page_article_url_list

        if page == limit:
            break

    driver.quit()

    logger.debug(f'{article_url_list=}')
    return article_url_list


def scrape_article_page(driver: webdriver.Chrome, url: str):
    driver.get(url)
    date = driver.find_element(
        by=By.CSS_SELECTOR,
        value='.topic-header__item.topic-header__time'
    ).get_attribute('href')[17:-1].replace('/', '-')
    logger.debug(f'{date=}')

    title = driver.find_element(By.TAG_NAME, 'h1').text
    logger.debug(f'{title=} {url=}')

    text = driver.find_element(By.CLASS_NAME, 'topic-body__content').text
    html_text = convert_article_parts_to_html(
        title=title,
        sub_title=None,
        text=text
    )
    image = get_article_image(driver)

    add_kyc_article(
        name=title,
        description=html_text,
        date=date,
        image=image,
        origin='https://lenta.ru/',
        source=url
    )


def scrape_lenta_ru_articles_chunk(article_url_list: list[str]):
    driver = get_driver()
    try:
        for article_url in article_url_list:
            scrape_article_page(
                driver=driver,
                url=article_url
            )
    finally:
        driver.quit()
