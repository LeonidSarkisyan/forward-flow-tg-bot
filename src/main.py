import logging
import asyncio

from aiogram import Bot, Dispatcher

from src.middlewares.base import ProtectMiddleware
from src.config import BOT_TOKEN
from src.handlers import systems, basic, posts, send, processing, admin, auth
from src.database import engine
from src.models import Base
from src.entities.users.service import role_service
from src.entities.password.service import password_service


async def start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await role_service.create_roles()
    await password_service.create_super_admin_password()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")

    dp = Dispatcher()

    protect_path = [admin.router, posts.router, basic.router, send.router, processing.router]

    dp.include_router(auth.router)

    for protect_router in protect_path:
        protect_router.message.middleware.register(ProtectMiddleware())
        protect_router.callback_query.middleware.register(ProtectMiddleware())
        dp.include_router(protect_router)

    dp.startup.register(systems.get_start)
    dp.shutdown.register(systems.get_stop)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

asyncio.run(start())
