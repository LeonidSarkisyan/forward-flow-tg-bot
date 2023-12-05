from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_password_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Ввести пароль", callback_data="enter_password")

    return inline_keyboard_builder.as_markup()
