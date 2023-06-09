import io

import requests

from server.config import logger, KYC_BASE_API_TOKEN


def add_kyc_article(
    name: str,
    description: str,
    date: str,
    image: io.BytesIO | None,
    origin: str,
    source: str,
) -> bool:
    data = {
        'name': name,
        'description': description,
        'source': source,
        'origin': origin,
        'date': date
    }

    response = requests.post(
        'https://kycbase.io/parsers/api/articles/',
        data=data,
        files={
            'image': image
        },
        headers={
            'Authorization': f'Token {KYC_BASE_API_TOKEN}'
        }
    )
    if response.status_code == 404:
        logger.error('KYC server is not responding')
        return

    json_response = response.json()
    article_id = json_response.get('id')

    if article_id is None:
        article_id = json_response.get('name')[0]
        logger.info(f'article already created {article_id=}')
        return False
    else:
        logger.success(f'article added successfully {article_id=}')
        return True
