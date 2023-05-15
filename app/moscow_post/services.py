import io
import re
import time
import uuid
import itertools
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from app.kyc import add_kyc_article


def get_article_image(driver: webdriver.Chrome, url: str) -> io.BytesIO:
    driver.get(url)
    image = io.BytesIO(driver.find_element(By.CSS_SELECTOR, 'img[src^=http]').screenshot_as_png)
    image.name = f'moscow-post-{uuid.uuid4().hex}.png'
    return image


def convert_article_parts_to_html(
    title: str,
    sub_title: str,
    text: str
) -> str:
    article_text = f'<h1>{title}</h1><h2>{sub_title}</h2>'

    text = re.sub(r'\n{2,}', '\n', text.strip()).split('\n')
    for paragraph in text:
        article_text += f'<p>{paragraph}</p>'
    return article_text


def scrape_article_page(driver: webdriver.Chrome, url: str):
    driver.get(url)
    print('page was loaded')

    published_time_string = driver.find_element(
        By.CSS_SELECTOR,
        'meta[property="article:published_time"]'
    ).get_attribute('content')[5:][:-15]
    date = datetime.strptime(published_time_string, '%d %b %Y').strftime('%Y-%m-%d')

    title = driver.find_element(By.TAG_NAME, 'h1').text
    sub_title = driver.find_element(By.TAG_NAME, 'h2').text
    text = driver.find_element(By.CLASS_NAME, 'article-text').text

    image_url = driver.find_element(By.CSS_SELECTOR, 'h2 + div img').get_attribute('src')
    image = get_article_image(
        driver=driver,
        url=image_url
    )

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
        origin=url,
        source='http://www.moscow-post.su/'
    )


options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)
driver.implicitly_wait(120)
driver.get('http://www.moscow-post.su/all/')
time.sleep(20)

for page in itertools.count(1):
    response = driver.execute_script(f'''
    return await (await fetch("http://www.moscow-post.su/all/?load=1&page={page}&start=15.11.2022&end=15.05.2023&sort=DESC", {{
        "headers": {{
            "accept": "*/*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
        }},
        "referrer": "http://www.moscow-post.su/all/",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": null,
        "method": "GET",
        "mode": "cors",
        "credentials": "include"
    }})).json();
    ''')
    print(response)
    if response['articles'] == []:
        break

    for article_item in response['articles']:
        url = 'http://www.moscow-post.su' + article_item['full_url']
        print(url)
        scrape_article_page(
            driver=driver,
            url=url
        )

driver.quit()