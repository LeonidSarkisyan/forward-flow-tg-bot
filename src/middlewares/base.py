import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from src.entities.password.service import password_service
from src.entities.users.service import user_service
from src.keyboards.auth import get_password_keyboard
from src.keyboards.basic import main_keyboard


class ProtectMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        user = await user_service.add_user(event.from_user.id, event.from_user.username)
        user = await user_service.get_user(event.from_user.id)
        if user.role_id == 4:
            if data["raw_state"] == "PasswordForm:get_password":
                auth = await password_service.login(event.text, event.from_user.id)
                if auth:
                    if auth.role_id == 1:
                        await event.answer(
                            "Вы зашли как <b>супер-админ</b>."
                        )
                    if auth.role_id == 2:
                        await event.answer(
                            "Вы зашли как <b>админ</b>.",
                            reply_markup=main_keyboard()
                        )
                else:
                    await event.answer("Неверный пароль!")
            else:
                await event.answer(
                    "Вы не имеете доступа к этому боту.",
                    reply_markup=get_password_keyboard()
                )
        else:
            await handler(event, data)
