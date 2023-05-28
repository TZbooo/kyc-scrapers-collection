import io
import uuid
import enum
from datetime import datetime

import requests

from scraper.config import logger, PROXY_CYCLE
from scraper.kyc import add_kyc_article


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

    logger.debug(f'{article_url=} {date=} {title=} {image=}')


def scrape_all_artciles_from_category(
    articles_count: int,
    category: ArticleCategories,
    chunks_limit: int | None = None,
    offset: int = 0
):
    step = 20
    for i, offset in enumerate(range(offset, articles_count + step, step)):
        if i == chunks_limit:
            break

        logger.debug(f'{i=} offset={offset}')
        articles = get_washington_post_articles(
            category=category,
            offset=offset
        )

        logger.debug('articles count ', len(articles['items']))
        for article_item in articles['items']:
            try:
                scrape_article_item(article_item)
            except Exception as e:
                logger.error(e)


def get_washington_post_articles(
    category: ArticleCategories,
    offset: int,
    limit: int = 20
) -> dict:
    headers = {
        'authority': 'www.washingtonpost.com',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'wp_devicetype=0; wp_ak_signinv2=1|20230125; wp_ak_wab=1|0|0|1|1|1|1|1|0|20230418; wp_ak_v_mab=0|0|0|20230429; wp_ak_v_ot=1; wp_ak_ot=1|20211012; wp_ak_bt=1|20200518; wp_ak_bfd=1|20201222; wp_ak_tos=1|20211110; wp_ak_sff=1|20220425; wp_ak_co=2|20220505; wp_ak_pp=1|20210310; _gaexp=GAX1.2.k6teSx_zRR6s8clzhm1AuQ.19557.1; wp_ak_pct=1|20230522; wp_pwapi_ar="H4sIAAAAAAAA/1XLuRGAMAwEwF4UE5xOtmzRDf4qIGPcO6TMbLqPKEdbEwwovMbKM2oHswUjTzkfueUU9ZqKV37CZR9StJPDuqMso9MvtKmG0Q3Nf60gMVmm7P0CufAP3W8AAAA="; wp_ak_lr=0|20221020; wp_ak_btap=1|20211118; wp_ak_subs=1|20230524; wp_usp=1---; _gid=GA1.2.1578700263.1685206641; OptanonAlertBoxClosed=2023-05-27T16:57:41.189Z; eupubconsent-v2=CPsayogPsayogAcABBENDGCkAP_AAH_AACiQGWQFwAKgAYABkAESAJoAnABuAHsAQgAnYBWYCvAK-AXUAwIBpgDiAHUAP0AfwBDACNQF5gMZAZYBlkA4ACoAMgAiAB-AHsAQgAiwBdQDAgHEAOoAvMBggDLAAAAA.f_gAD_gAAAAA; wp_ucp=|EAC:1|; __gads=ID=525b76a8cbb698d1:T=1685206661:RT=1685207101:S=ALNI_MZlbJke7A51htvG--P0C2GweX32xg; wp_geo=RU||||INTL; ak_bmsc=E428F3D53F9A5D7D2C80091DBCD489E8~000000000000000000000000000000~YAAQnjxRaGAmeTSIAQAA34b5YhPnxRIUTxL08McuZnkODjsFUKJukTQbFub1txjQv9Aoa/norAKiwmI6dKzOGwA6tMIYAG0j6iWr4dnunNpOk3yjGLvVIv/cQoYBXysSdc4tPgqqFIh4f7WNr1CCFJUFycvDtoGqNq0XCvou+0AOM84C7PHZBJOnvt0Yb8Xjch2h6iHz0xxuQUTlGiJGbDi1uEo1PC7E7W7ovv/RiXqttjVz4lPQkkK2nqKPE1fsRV8WlP3CV+vYHf2y5evA6q1J3+Xp1FyN7I3jkmZyltzUGO7D8+bMWvI7LIOnY7SykHMJ6EEuh+AskFx9BaR6h12NEUm1pWf1HMmWxdBYGnzk9Lb2hH+MfyTFb8i9qwaZbV/Ea9wTX6GVqVI2wl1cnqOb8g==; permutive-id=52b2fbee-579b-4899-b184-aa327d276bd1; _cb=Bd2Ju8BX3kNjCvqCHo; _cb_svref=null; _fbp=fb.1.1685287710008.9093095211; jctr_sid=4094168528771003917540; jts-rw={"u":"55905168473507470157971"}; jts-fbp=fb.1.1685287710008.9093095211; OptanonConsent=isGpcEnabled=0&datestamp=Sun+May+28+2023+18%3A29%3A02+GMT%2B0300+(Moscow+Standard+Time)&version=202210.1.0&isIABGlobal=false&hosts=&consentId=eaaf9406-af2e-4d59-9877-73a64aa95bab&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&iType=1&geolocation=NL%3B&AwaitingReconsent=false; bm_sv=3B4B3DCBAD7AB80E0942B14D8A777FEC~YAAQnjxRaG+FeTSIAQAAzh38YhPLTVh08w7i3KIGgSh6sAndosnSnNGDikhko55NZ8pxgX3MBVfVc0Mc3HJiRk4e62I5Ffk+7oeUEaLrLH9+iVWWBkDhxFJke2jX+af7fofsvzdUiysWZtMY7Ym89l5zYDQjwVfSm/sqeuyVNyfqpMI6tn9H6M5mAkf+BHZ33k8hE0W+6LBJvkSOrGJvUxSVn8E57UrKcgyt3Tqy1kjtg4P5ULpvNr1NXOv/4Fw+gx6q2DDHwMYB~1; _chartbeat2=.1684735168628.1685287870253.1011011.Lr7GYD0ZDdUCuMsuJCDOGX0C2XaBa.2; _chartbeat5=; _ga_WRCN68Y2LD=GS1.1.1685287709.1.1.1685287870.0.0.0; _ga=GA1.2.185135300.1684735092; cto_bundle=fvASF19lMzRjWFJrRlppY2lybjQ3OVVBJTJCb2piU0R2JTJGOSUyQiUyRnlMTnclMkZGUTVJSGJUbjlKZlBOUVFZZ2Zacmo0WHlidHMzZVNDQ2x3YVNhSzB3eFRqYTg2MVlTY3UlMkZjZ3g1UyUyRlBPUG1wZTdmbVVISFUydzhiTlZwV1ZDZ0xOazdaSEt6QkZhWVU5WGxmWHhXMGJIUzlFUk5JMTNucjlxd2NFVWU4WW96SGN4NUpjdWtIWSUzRA',
        'referer': f'https://www.washingtonpost.com/national/investigations/?itid=nb_{category.name}',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    params = {
        '_website': 'washpost',
    }

    proxies = {
        'https': next(PROXY_CYCLE)
    }

    if category.name == 'investigations':
        params['query'] = f'{{"query":"prism://prism.query/site,/national/investigations&offset={offset}&limit={limit}"}}'
    else:
        params['query'] = f'{{"query":"prism://prism.query/site-articles-only,/{category.name}/&offset={offset}&limit={limit}"}}'
    
    response = requests.get(
        'https://www.washingtonpost.com/prism/api/prism-query',
        headers=headers,
        params=params,
        proxies=proxies
    )
    logger.debug(f'{response.status_code=} {response.request.path_url}')
    return response.json()
