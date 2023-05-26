import io
import uuid
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from scraper.config import logger, BLOCK_BYPASS_PROXY
from scraper.kyc import add_kyc_article


cookies = {
    'Path': '/',
    'Path': '/',
    'fs.bot.check': 'true',
    '_fbp': 'fb.1.1685040253878.806680330',
    '_gid': 'GA1.2.385673895.1685040255',
    'euconsent-v2': 'CPsUnIAPsUnIAAKAvAENDFCsAP_AAH_AABpYJbtX_H__bW9r8f5_aft0eY1P9_j77uQzDhfNk-4F3L_W_JwX52E7NF36tq4KmR4Eu3LBIUNlHNHUTVmwaokVryHsak2cpTNKJ6BEkHMRO2dYGF5umxtjeQKY5_p_d3fx2D-t_dv-39z3z81Xn3dZf-_0-PCdU5_9Dfn9fRfb-9IL9_78v8v8_9_rk2_eX_3_79_7_H9-f_84JcAEmGrcQBdmUODNoGEUCIEYVhARQKACCgGFogIAHBwU7IwCfWESAFAKAIwIgQ4AoyIBAAAJAEhEAEgRYIAAABAIAAQAIBEIAGBgEFABYCAQAAgOgYohQACBIQJEREQpgQFQJBAS2VCCUF0hphAFWWAFAIjYKABEEgIrAAEBYOAYIkBKxYIEmINogAGAFAKJUK1FJ6aAhYzMAAAA.YAAAAAAAAAAA',
    'addtl_consent': '1~39.4.3.9.6.9.13.6.4.15.9.5.2.11.1.7.1.3.2.10.3.5.4.21.4.6.9.7.10.2.9.2.18.7.20.5.20.6.5.1.4.11.29.4.14.4.5.3.10.6.2.9.6.6.9.4.4.29.4.5.3.1.6.2.2.17.1.17.10.9.1.8.6.2.8.3.4.146.8.42.15.1.14.3.1.18.25.3.7.25.5.18.9.7.41.2.4.18.21.3.4.2.7.6.5.2.14.18.7.3.2.2.8.20.8.8.6.3.10.4.20.2.13.4.6.4.11.1.3.22.16.2.6.8.2.4.11.6.5.33.11.8.1.10.28.12.1.3.21.2.7.6.1.9.30.17.4.9.15.8.7.3.6.6.7.2.4.1.7.12.13.22.13.2.12.2.10.1.4.15.2.4.9.4.5.4.7.13.5.15.4.13.4.14.10.15.2.5.6.2.2.1.2.14.7.4.8.2.9.10.18.12.13.2.18.1.1.3.1.1.9.25.4.1.19.8.4.5.3.5.4.8.4.2.2.2.14.2.13.4.2.6.9.6.3.2.2.3.5.2.3.6.10.11.6.3.16.3.11.3.1.2.3.9.19.11.15.3.10.7.6.4.3.4.6.3.3.3.3.1.1.1.6.11.3.1.1.11.6.1.10.5.2.6.3.2.2.4.3.2.2.7.15.7.14.1.3.3.4.5.4.3.2.2.5.4.1.1.2.9.1.6.9.1.5.2.1.7.10.11.1.3.1.1.2.1.3.2.6.1.12.5.3.1.3.1.1.2.2.7.7.1.4.1.2.6.1.2.1.1.3.1.1.4.1.1.2.1.8.1.7.4.3.2.1.3.5.3.9.6.1.15.10.28.1.2.2.12.3.4.1.6.3.4.7.1.3.1.1.3.1.5.3.1.3.4.1.1.4.2.1.2.1.2.2.2.4.2.1.2.2.2.4.1.1.1.2.2.1.1.1.1.2.1.1.1.2.2.1.1.2.1.2.1.7.1.2.1.1.1.2.1.1.1.1.2.1.1.3.2.1.1.8.1.1.6.2.1.6.2.3.2.1.1.1.2.2.3.1.1.4.1.1.2.2.1.1.4.3.1.2.2.1.2.1.2.3.1.1.2.4.1.1.1.5.1.3.6.3.1.5.2.3.4.1.2.3.1.4.2.1.2.2.2.1.1.1.1.1.1.11.1.3.1.1.2.2.5.2.3.3.5.1.1.1.4.2.1.1.2.5.1.9.4.1.1.3.1.7.1.4.5.1.7.2.1.1.1.2.1.1.1.4.2.1.12.1.1.3.1.2.2.3.1.2.1.1.1.2.1.1.2.1.1.1.1.2.4.1.5.1.2.4.3.8.2.2.9.7.2.2.1.2.1.4.6.1.1.6.1.1.2.6.3.1.2.201.300.100',
    '_pbjs_userid_consent_data': '6838263375797728',
    '_iiq_fdata': '%7B%22pcid%22%3A%227a3ec4c3-86c2-4093-a4fc-7710d19346ea%22%7D',
    'cookie': 'ea08ce9c-52da-4e14-8170-f38de5051699',
    '_lr_env_src_ats': 'false',
    '_cc_id': '59a45c157360d09681b0a82dfb75f04b',
    'panoramaId_expiry': '1685645062634',
    'panoramaId': '978fcbf3d6934880d9dfd3aad46316d5393880b6b40ce4bdfd9fdca29b7e0994',
    'panoramaIdType': 'panoIndiv',
    '__qca': 'P0-604665960-1685040261421',
    '_lr_retry_request': 'true',
    'AMP_TOKEN': '%24NOT_FOUND',
    '__gads': 'ID=e5ac112ed461d08b:T=1685040261:RT=1685117360:S=ALNI_Mbqgfz2gK4rjyBJ09aqiv4S8WQkmg',
    '__gpi': 'UID=00000c1c09107772:T=1685040261:RT=1685117360:S=ALNI_Mb61cO63c9yQk6kjasEPE1MK6IUtg',
    '_dc_gtm_UA-4186815-1': '1',
    '_ga': 'GA1.1.823263633.1685040252',
    '_ga_7PDWRZPVQJ': 'GS1.1.1685116805.3.1.1685117372.60.0.0',
    '_awl': '2.1685117373.5-dd6e7910190635675b1619c32f5bbea1-6763652d6575726f70652d7765737431-0',
    'cto_bidid': 'gDs4MV80bEtzOGlnQVc1TjR2dmVzbXB6akkyc01iaFFjdHljSWVVSlRBYTdOUndLaHpwV3hZc0lxZU5ZWENYbm5ySFVMRHFmVzdyM0pmOGlHYmk3dmElMkZBV2drNHNDeld6ak84d0lMZnNuQUJoeiUyQllrN1BueCUyQks2QnpLdnVxJTJCWElDTHUx',
    'cto_bundle': 'rBsiKl9FZkRvcHJoNUVkSDB2czN6WmZlc2slMkZpYkJ4dkJtN3ZtR3FqVGQzM3pYUEVJWk1SOUYxblNham1OMENPSFBlc2JsZldWUkhYTU1WZGtTejA1STRTRm1ac2NTSVc4U01IJTJGaWE3enEwV2hGeGNXNm5tQXFMR0ZTOWtlckdXZ05INFFyazQyUWNGRXVoZWduSjclMkI4N25LJTJCeHA3UE9TYjFVZVRBdUJEeWZLb29ZdyUzRA',
}

headers = {
    'authority': 'www.themoscowtimes.com',
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://www.themoscowtimes.com/news',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

proxies = {
    'http': BLOCK_BYPASS_PROXY,
    'https': BLOCK_BYPASS_PROXY
}


def convert_article_parts_to_html(title: str, soup: BeautifulSoup) -> str:
    html_text = f'<h1>{title}</h1>'
    article_block_list = soup.select_one('.article__content .article__block--html')

    for article_block in article_block_list:
        if not article_block.text.strip():
            continue
        html_text += str(article_block).strip()
    return html_text


def get_article_url_list(page: int) -> list[str]:
    logger.info(f'start scraping page {page} articles')

    html = requests.get(
        f'https://www.themoscowtimes.com/news/{1 + 18 * page}',
        cookies=cookies,
        headers=headers,
        proxies=proxies
    ).text
    soup = BeautifulSoup(html, 'html.parser')

    return [article['data-url'] for article in soup.select('.article-excerpt-default')]


def scrape_article_page(url: str):
    html = requests.get(
        url,
        cookies=cookies,
        headers=headers,
        proxies=proxies
    ).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content'].replace(' - The Moscow Times', '')
    date = datetime.fromisoformat(
        soup.select_one('meta[property="article:published_time"]')['content']
    ).strftime('%Y-%m-%d')

    image_url = soup.select_one('meta[property="og:image"]')['content']
    image = io.BytesIO(requests.get(image_url, proxies=proxies).content)
    image.name = f'themoscowtimes-{uuid.uuid4().hex}.jpg'

    html_text = convert_article_parts_to_html(
        title=title,
        soup=soup
    )

    logger.debug(f'{title=} {url=} {date=} {image=} {html_text=}')
    add_kyc_article(
        name=title,
        description=html_text,
        date=date,
        image=image,
        origin='https://www.themoscowtimes.com/',
        source=url
    )
