import asyncio
import os
import random
import time
from bs4 import BeautifulSoup
from datetime import datetime

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.media_group import MediaGroupBuilder

from src.config import POSTS_CHANNEL_ID, ADMIN_ID
from src.entities.media.service import media_service
from src.entities.flow.service import flow_service
from src.entities.setting.service import setting_service


router = Router()

F: Message


class PostForm(StatesGroup):
    get_post = State()


def get_newest_folder(path):
    newest = None
    date = None

    for f in get_all_files(path):
        if date == None or date < os.path.getmtime(f"media_list/{f}"):
            newest = f
            date = os.path.getmtime(f"media_list/{f}")

    return os.path.join(path, newest)


def get_all_files(path):
    return [x for x in os.listdir(path) if not os.path.isfile(x)]


HTML_TEXT = ""


@router.channel_post(F.text.startswith("chat_id__"), F.chat.id == POSTS_CHANNEL_ID)
async def get_post_and_send(message: Message, bot: Bot):
    global HTML_TEXT
    time.sleep(4)
    parsed_channel_id = int(message.text.split("__")[1])

    flow = await flow_service.get_flow_by_parsed_channel_id(parsed_channel_id)

    last_media = await media_service.get_last_media()
    media = await media_service.get_media(last_media.media_group_id)

    media_list = [media_object for media_object in media]

    try:
        caption = [media_item.caption for media_item in media_list if media_item.caption][0]
    except IndexError:
        caption = ""

    if len(HTML_TEXT) > 0:
        caption = HTML_TEXT

    album_builder = MediaGroupBuilder(caption=caption)

    HTML_TEXT = ""

    is_media = True

    for media_object in media_list:
        if media_object.type == "photo":
            album_builder.add_photo(media=media_object.file_id)
        elif media_object.type == "video":
            album_builder.add_video(media=media_object.file_id)
        elif media_object.type == "text":
            is_media = False
            break

    print("ВСЕ КАНАЛЫ КУДА НУЖНО ОТПРАВИТЬ ЭТОТ ПОСТ:")
    for flow_item in flow:
        receiver_channel_id = flow_item.receiver_channel_id

        settings = await setting_service.get_settings(receiver_channel_id)

        if settings.change_link:
            soup = BeautifulSoup(caption if is_media else media_list[0].file_id, features="html5lib")
            for a in soup.findAll('a'):
                a['href'] = settings.link
            if is_media:
                album_builder.caption = str(soup).replace(
                    "<html><head></head><body>", ""
                ).replace("</body></html>", "")
            else:
                media_list[0].file_id = str(soup).replace(
                    "<html><head></head><body>", ""
                ).replace("</body></html>", "")

        if settings.deleted_key_words:
            deleted_words = settings.deleted_key_words.split("&&")
            print(f"СЛОВА КОТОРЫЕ НУЖНО УДАЛИТЬ: {deleted_words}")
            text = album_builder.caption if is_media else media_list[0].file_id
            for deleted_word in deleted_words:
                print(text)
                text = text.replace(deleted_word, "")
            if is_media:
                album_builder.caption = text
            else:
                media_list[0].file_id = text

        if settings.postscript:
            text: str = album_builder.caption if is_media else media_list[0].file_id
            count_enter = 0
            try:
                start_index_enter = text[::-1].index("\n")
            except ValueError:
                start_index_enter = 0

            with_out_text = text[:-start_index_enter]

            for symbol in with_out_text[::-1]:
                if symbol == "\n":
                    count_enter += 1
                else:
                    break
            print("Количество переносов:")
            print(count_enter)

            count_enter = 2 - count_enter
            enter = "\n" * count_enter

            text = text + f"{enter}{settings.postscript}"
            if is_media:
                album_builder.caption = text
            else:
                media_list[0].file_id = text

        print(receiver_channel_id)
        if is_media:
            await bot.send_media_group(
                receiver_channel_id, album_builder.build()
            )
        else:
            await bot.send_message(
                receiver_channel_id,
                media_list[0].file_id,
                disable_web_page_preview=True
            )

    print("НУЖНО УДАЛИТЬ:")
    print(last_media.media_group_id)


GLOBAL_NAME_FILES = 1000


@router.channel_post(F.text.startswith("userbot__html__text__"))
async def get_html_text(message: Message):
    global HTML_TEXT
    HTML_TEXT = message.html_text.split("__")[-1]
    print(f"HTML TEXT - {message.html_text.split('__')[-1]}")


@router.channel_post(F.text)
async def get_text(message: Message):
    await media_service.create_media("text", message.html_text, message.message_id, datetime.now())


@router.channel_post(F.chat.id == POSTS_CHANNEL_ID, F.content_type)
async def get_media(message: Message, bot: Bot):
    try:
        os.mkdir(f"src/media_list/{message.media_group_id}")
    except FileExistsError:
        pass

    time.sleep(0.25)
    datetime_now = datetime.now()
    print(datetime_now)

    caption = message.html_text if message.html_text else ""

    print("Медиагруппа:", message.media_group_id)

    id_ = message.media_group_id if message.media_group_id else message.message_id

    if message.photo:
        photo_id = message.photo[-1].file_id
        await media_service.create_media(
            "photo", photo_id, id_, datetime_now, caption
        )
    if message.video:
        video_id = message.video.file_id
        await media_service.create_media(
            "video", video_id, id_, datetime_now, caption
        )
    if message.animation:
        animation_id = message.animation.file_id
        await media_service.create_media(
            "animation", animation_id, id_, datetime_now, caption
        )
