import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


def get_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(
        service=ChromeService('/code/chromedriver'),
        options=options
    )
    driver.implicitly_wait(30)
    driver.set_script_timeout(30)
    return driver


def convert_article_parts_to_html(
    title: str | None,
    sub_title: str | None,
    text: str
) -> str:
    article_text = ''
    if title:
        article_text += f'<h1>{title}</h1>'
    if sub_title:
        article_text += f'<h2>{sub_title}</h2>'

    text = re.sub(r'\n{2,}', '\n', text.strip()).split('\n')
    for paragraph in text:
        article_text += f'<p>{paragraph}</p>'
    return article_text