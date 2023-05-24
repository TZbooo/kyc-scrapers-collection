from app.worker import celery
from app.bsslib import get_driver
from .services import get_washington_post_articles, scrape_article_item


@celery.task(name='scrape_washington_post_task')
def scrape_washington_post_task() -> bool:
    driver = get_driver()
    driver.get('https://www.washingtonpost.com/world/?itid=nb_world')

    articles_count = get_washington_post_articles(
        driver=driver,
        offset=0,
        limit=1
    )['count']
    for i in range(0, articles_count + 20, 20):
        articles = get_washington_post_articles(
            driver=driver,
            offset=i,
            limit=i + 20
        )

        for article_item in articles['items']:
            scrape_article_item(article_item)
        driver = get_driver()
        driver.get('https://www.washingtonpost.com/world/?itid=nb_world')
    return True
