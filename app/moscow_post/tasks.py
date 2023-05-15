import time
import itertools

from app.config import logger
from app.worker import celery
from .services import get_driver, scrape_article_page


@celery.task(name='scrape_moscow_post_articles_chunk_task')
def scrape_moscow_post_articles_chunk_task(article_url_list: list[str]) -> bool:
    driver = get_driver()

    try:
        for article_url in article_url_list:
            logger.info(f'start scraping {article_url}')
            scrape_article_page(
                driver=driver,
                url=article_url
            )
            time.sleep(1)
    finally:
        driver.quit()
    return True


@celery.task(name='scrape_moscow_post_task')
def scrape_moscow_post_task() -> bool:
    driver = get_driver()

    try:
        driver.get('http://www.moscow-post.su/all/')
        logger.info('wait for page load')
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
            logger.trace(response)
            if response['articles'] == []:
                break

            article_url_list = [
                'http://www.moscow-post.su' + article_item['full_url']
                for article_item in response['articles']
            ]
            scrape_moscow_post_articles_chunk_task.apply_async(kwargs={'article_url_list': article_url_list})
    finally:
        driver.quit()
    return True