from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import (
    UsernameInvalid, UsernameNotOccupied, PeerIdInvalid
)
from pyrogram.enums.parse_mode import ParseMode

from src.config import POSTS_CHANNEL_ID
from src.entities.parsed_channels.service import parsed_channel_service


async def get_operation(operation, arg: str, user_id: int, client: Client, message: Message):
    if operation == "add":
        async def add_channel():
            channel_name = arg.split("/")[-1]
            print("Подписываемся на", channel_name)
            try:
                chat = await client.join_chat(channel_name)
            except UsernameInvalid:
                await client.send_message(
                    POSTS_CHANNEL_ID,
                    f"userbot__error__invalid__{user_id}",
                    parse_mode=ParseMode.DISABLED
                )
            except UsernameNotOccupied:
                await client.send_message(
                    POSTS_CHANNEL_ID,
                    f"userbot__error__notfound__{user_id}",
                    parse_mode=ParseMode.DISABLED
                )
            except PeerIdInvalid:
                await client.send_message(
                    POSTS_CHANNEL_ID,
                    f"userbot__error__invalid__{user_id}",
                    parse_mode=ParseMode.DISABLED
                )
            else:
                channel_id = chat.id
                channel_username = chat.username
                await client.send_message(
                    POSTS_CHANNEL_ID,
                    f"userbot__add__{channel_id}__{channel_username}__{user_id}",
                    parse_mode=ParseMode.DISABLED
                )
        return add_channel
