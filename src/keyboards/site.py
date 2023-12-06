from aiogram.utils.keyboard import InlineKeyboardBuilder


def control_site_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(
        text="Проверить наличие новых постов", callback_data="check_site_content"
    )
    inline_keyboard_builder.button(text="")
    