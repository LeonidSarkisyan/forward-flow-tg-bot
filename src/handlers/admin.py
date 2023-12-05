from aiogram import Router, Bot, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.keyboards.admin import get_admin_menu_keyboard
from src.entities.password.service import password_service
from src.entities.users.service import user_service


router = Router()


@router.callback_query(F.data == "control_admin")
async def ask_password(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Вы зашли в админку",
        reply_markup=get_admin_menu_keyboard()
    )
    await call.answer()


@router.callback_query(F.data == "create_password_for_admin")
async def create_admin_password(call: CallbackQuery):
    password = await password_service.create_password(40)
    await call.message.answer(
        f"Созданный пароль: <code>{password}</code>\n\n"
        f"После того, как пользователь введёт этот пароль, он самоуничтожится."
    )
    await call.answer()


@router.callback_query(F.data == "all_admins")
async def get_admins(call: CallbackQuery):
    admins = await user_service.get_admins()
    print(admins)
