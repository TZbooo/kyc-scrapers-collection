import uuid
import re
import io

from bs4 import BeautifulSoup
from telethon import types

from app.config import logger, SCRAPING_CONF
from app.kyc import add_kyc_article


def get_message_image(message: types.Message) -> io.BytesIO:
    if isinstance(message.media, types.MessageMediaPhoto):
        image = io.BytesIO(message.download_media(file=bytes))
        image.name = f'{message.id}-{uuid.uuid4().hex}.jpg'
        return image


def convert_description_to_paragraphs(description: str) -> str:
    paragraph_list = ''
    for paragraph in description.strip().replace('\n\n', '\n').split('\n'):
        paragraph_list += f'<p>{paragraph}</p>'
    return paragraph_list


def delete_source_names_from_text(channel: types.Channel, message: types.Message, text: str) -> str:
    text = text.replace(channel.title, '')
    text = text.replace('Дорогие подписчики и гости канала!', '')

    try:
        forwarded_channel_name = message.forward.chat.title
        text = text.replace(forwarded_channel_name, '')
    except AttributeError:
        pass
    return text


def get_username_from_channel_link(channel_link: str) -> str:
    return channel_link.replace('https://t.me/', '').replace('/', '')


def get_scraper_conf_by_channel_username(channel_username: str) -> dict:
    for scraper in SCRAPING_CONF:
        if channel_username == get_username_from_channel_link(scraper['channel_link']):
            return scraper


@logger.catch
def scrape_message(
    min_characters: int,
    message: types.Message,
    channel: types.Channel
):
    if not message.text:
        logger.info('text not found, skip')
        return

    text = BeautifulSoup(message.text, 'lxml').text
    if len(text) < min_characters:
        logger.info('message hasn\'t min characters, skip')
        return
    
    text = delete_source_names_from_text(
        channel=channel,
        message=message,
        text=text
    )

    article_groups = re.search(r'(^.+?[\n\.:])(.+)', text, flags=re.DOTALL)
    try:
        name = article_groups.group(1).strip()
        description = f'{name}\n{article_groups.group(2).strip()}'
    except AttributeError:
        logger.info(f'regex not found in {text=}')
        return

    description = convert_description_to_paragraphs(description)
    article_date = message.date.strftime('%Y-%m-%d')
    image = get_message_image(message)

    add_kyc_article(
        name=name,
        description=description,
        date=article_date,
        image=image,
        message=message,
        channel=channel
    )
