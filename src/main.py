import logging
import asyncio

from aiogram import Bot, Dispatcher

from src.config import BOT_TOKEN
from src.handlers import systems, basic
from src.database import engine
from src.models import Base
from src.entities.users.service import role_service


async def start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await role_service.create_roles()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")

    dp = Dispatcher()

    dp.include_router(basic.router)

    dp.startup.register(systems.get_start)
    dp.shutdown.register(systems.get_stop)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

asyncio.run(start())
