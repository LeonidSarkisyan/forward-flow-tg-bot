import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from src.config import API_ID, API_HASH


client = Client("my_account", API_ID, API_HASH)


@client.on_message()
def send_stat(client_: Client, message: Message):
    client_.copy_message(-1002042549831, message.chat.id, message.id)


client.run()

