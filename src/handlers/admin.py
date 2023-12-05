from aiogram import Router, Bot, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.keyboards.admin import get_admin_menu_keyboard, admin_list_keyboard, admin_delete_list
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
    admin_list_string = ""

    for admin in admins:
        admin_list_string += f"@{admin.username}"

    await call.message.edit_text(
        "Список ваших админов:\n\n"
        f"{admin_list_string}",
        reply_markup=admin_list_keyboard()
    )
    await call.answer()


@router.callback_query(F.data == "delete_admin_list")
async def delete_list_admin(call: CallbackQuery):
    admins = await user_service.get_admins()
    print(admins)
    await call.message.edit_text(
        "Кликните по тому админу, которого вы хотите удалить:",
        reply_markup=admin_delete_list(admins)
    )


@router.callback_query(F.data.startswith("delete_admin_one__"))
async def delete_one_admin(call: CallbackQuery):
    admin_id = call.data.split("__")[-1]
    await user_service.delete_admin(admin_id)
    admins = await user_service.get_admins()
    await call.answer(f"Админ был удалён.")
    await call.message.edit_reply_markup(reply_markup=admin_delete_list(admins))


CONFIRMATION_TEXT = "Я хочу выйти из аккаунта супер-юзера"


class LogOutForm(StatesGroup):
    get_confirm_text = State()


@router.callback_query(F.data == "logout_super_admin")
async def logout_super_admin(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        "Вы действительно хотите выйти из аккаунта супер-админа?\n\n"
        "Вам будет отправлен новый пароль, с помощью которого вы сможете "
        "вернуться или дать доступ другому пользователю"
    )
    await call.message.answer(
        "Для подтверждения выхода напишите этот текст:\n\n"
        f"<i>{CONFIRMATION_TEXT}</i>")
    await state.set_state(LogOutForm.get_confirm_text)


@router.message(LogOutForm.get_confirm_text, F.text)
async def get_confirm_text(message: Message, state: FSMContext):
    if message.text == CONFIRMATION_TEXT:
        password = await password_service.create_super_admin_password()
        await message.answer(f"Новый пароль для супер админа: <code>{password}</code>")
        await message.answer(f"Будьте осторожны! Делитесь с паролем только тому, кому вы сможете доверять!")
        await state.clear()
        await password_service.admin_to_user(message.from_user.id)
    else:
        await message.answer("Вы написали что-то другое, отменяю выход...")
        await state.clear()
