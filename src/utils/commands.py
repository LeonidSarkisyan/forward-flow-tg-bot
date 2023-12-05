from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Главное меню'
        ),
        BotCommand(
            command="parsed_channels",
            description="Список каналов, откуда парсится информация"
        ),
        BotCommand(
            command="new_parsed_channel",
            description="Добавить канал, откуда парсится информация"
        ),
        BotCommand(
            command="delete_parsed_channel",
            description="Удалить каналы, откуда парсится информация"
        ),
        BotCommand(
            command="receiver_channels",
            description="Список моих каналов"
        ),
        BotCommand(
            command="new_receiver_channel",
            description="Добавить свой канал"
        ),
        BotCommand(
            command="delete_receiver_channel",
            description="Удалить свой канал"
        )
    ]

    await bot.set_my_commands(commands)
