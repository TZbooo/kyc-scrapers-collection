import io
import re
import uuid
import pytz
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from app.config import logger, PROXY_CYCLE
from app.kyc import add_kyc_article


def get_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    proxy = next(PROXY_CYCLE)
    logger.info(f'current {proxy=}')

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(120)
    return driver


def get_article_image(driver: webdriver.Chrome) -> io.BytesIO | None:
    try:
        image_url = driver.find_element(By.CSS_SELECTOR, 'h2 + div img').get_attribute('src')
        driver.get(image_url)

        image = io.BytesIO(driver.find_element(By.CSS_SELECTOR, 'img[src^=http]').screenshot_as_png)
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


def convert_article_parts_to_html(
    title: str,
    sub_title: str | None,
    text: str
) -> str:
    article_text = f'<h1>{title}</h1>'
    if sub_title:
        article_text += f'<h2>{sub_title}</h2>'

    text = re.sub(r'\n{2,}', '\n', text.strip()).split('\n')
    for paragraph in text:
        article_text += f'<p>{paragraph}</p>'
    return article_text


def scrape_article_page(driver: webdriver.Chrome, url: str):
    driver.get(url)
    logger.info('page was loaded')

    published_time_string = driver.find_element(
        By.CSS_SELECTOR,
        'meta[property="article:published_time"]'
    ).get_attribute('content')[5:][:-15]
    date = datetime.strptime(published_time_string, '%d %b %Y').strftime('%Y-%m-%d')

    title = driver.find_element(By.TAG_NAME, 'h1').text
    logger.debug(f'{title=} {url=}')

    try:
        sub_title = driver.find_element(By.TAG_NAME, 'h2').text
    except NoSuchElementException:
        sub_title = None

    text = driver.find_element(By.CLASS_NAME, 'article-text').text
    image = get_article_image(driver)
    html_text = convert_article_parts_to_html(
        title=title,
        sub_title=sub_title,
        text=text
    )

    add_kyc_article(
        name=title,
        description=html_text,
        date=date,
        image=image,
        origin='http://www.moscow-post.su/',
        source=url
    )
