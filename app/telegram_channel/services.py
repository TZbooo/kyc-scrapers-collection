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
    

async def get_message_image_async(message: types.Message) -> io.BytesIO:
    if isinstance(message.media, types.MessageMediaPhoto):
        image = io.BytesIO(await message.download_media(file=bytes))
        image.name = f'{message.id}-{uuid.uuid4().hex}.jpg'
        return image


def convert_description_to_paragraphs(description: str) -> str:
    paragraph_list = ''
    for paragraph in re.sub(r'\n{2,}', '\n', description.strip()).split('\n'):
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
    for scraper in SCRAPING_CONF['telegram']:
        if channel_username == get_username_from_channel_link(scraper['channel_link']):
            return scraper
        

def get_article_name_and_description(
    message: types.Message,
    channel: types.Channel,
    min_characters: int
) -> list[str] | None:
    '''return: list[name: str, description: str] | None'''

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
        return name, description
    except AttributeError:
        logger.info(f'regex not found in {text=}')
        return


@logger.catch
def scrape_message(
    min_characters: int,
    message: types.Message,
    channel: types.Channel
):
    name_and_description = get_article_name_and_description(
        message=message,
        channel=channel,
        min_characters=min_characters
    )
    if name_and_description is None:
        return
    name, description = name_and_description

    description = convert_description_to_paragraphs(description)
    article_date = message.date.strftime('%Y-%m-%d')
    image = get_message_image(message)

    origin = f'https://t.me/{channel.username}/'
    source = f'{origin}{message.id}/'

    logger.info(f'start article adding {message.id=}')
    add_kyc_article(
        name=name,
        description=description,
        date=article_date,
        image=image,
        origin=origin,
        source=source
    )


@logger.catch
async def scrape_message_async(
    min_characters: int,
    message: types.Message,
    channel: types.Channel
):
    name_and_description = get_article_name_and_description(
        message=message,
        channel=channel,
        min_characters=min_characters
    )
    if name_and_description is None:
        return
    name, description = name_and_description

    description = convert_description_to_paragraphs(description)
    article_date = message.date.strftime('%Y-%m-%d')
    image = await get_message_image_async(message)

    add_kyc_article(
        name=name,
        description=description,
        date=article_date,
        image=image,
        message=message,
        channel=channel
    )
