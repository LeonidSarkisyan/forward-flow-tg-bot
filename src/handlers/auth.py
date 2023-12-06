from aiogram import Router, Bot, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.keyboards.basic import main_keyboard
from src.entities.password.service import password_service


router = Router()


class PasswordForm(StatesGroup):
    get_password = State()


@router.callback_query(F.data == "enter_password")
async def ask_password(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите пароль:")
    await state.set_state(PasswordForm.get_password)
    await call.answer()


@router.message(PasswordForm.get_password, F.text)
async def get_password(message: Message, state: FSMContext):
    auth = await password_service.login(message.text, message.from_user.id)
    if auth:
        if auth.role_id == 1:
            await message.answer(
                "Вы зашли как <b>супер-админ</b>.",
                reply_markup=main_keyboard(auth.role_id)
            )
        if auth.role_id == 2:
            await message.answer(
                "Вы зашли как <b>админ</b>.",
                reply_markup=main_keyboard(auth.role_id)
            )
    else:
        await message.answer("Неверный пароль! Нажми кнопку входа и попробуйте заново.")
        await state.clear()
