import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums.parse_mode import ParseMode

from src.config import API_ID, API_HASH, POSTS_CHANNEL_ID
from src.commands import get_operation


client = Client("my_account", API_ID, API_HASH)


@client.on_message(filters.chat(chats=int(POSTS_CHANNEL_ID)))
async def send_stat(client_: Client, message: Message):
    try:
        bot_tag, operation, arg, user_id = message.text.split("__")
    except ValueError:
        print("Сообщение не от бота")
    else:
        print("лол")
        if bot_tag == "bot":
            operation = await get_operation(operation, arg, int(user_id), client, message)
            await operation()


count_media_group = 0
text = ""


@client.on_message()
async def send_stat(client_: Client, message: Message):
    global count_media_group
    global text
    try:
        media_group = await client_.get_media_group(message.chat.id, message.id)
    except ValueError:
        try:
            await client_.copy_message(POSTS_CHANNEL_ID, message.chat.id, message.id)
        except ValueError:
            print(f"Нельзя скопировать сообщение - message id: {message.id}")
        else:
            await asyncio.sleep(2)
            await client_.send_message(
                POSTS_CHANNEL_ID, f"chat_id__{message.chat.id}",
                parse_mode=ParseMode.DISABLED
            )
    else:
        count_media_group += 1
        if message.caption:
            text = message.caption.html
            print("ТЕКСТ:", text)
        if len(media_group) == count_media_group:
            await client_.copy_media_group(
                POSTS_CHANNEL_ID, message.chat.id, message.id
            )
            await client_.send_message(
                POSTS_CHANNEL_ID, f"userbot__html__text__{text}", parse_mode=ParseMode.HTML
            )
            await asyncio.sleep(2)
            await client_.send_message(
                POSTS_CHANNEL_ID,
                f"chat_id__{message.chat.id}",
                parse_mode=ParseMode.DISABLED
            )
            count_media_group = 0
            text = ""


asyncio.run(client.run())
