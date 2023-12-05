from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_menu_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(
        text="Создать пароль для админа", callback_data="create_password_for_admin"
    )

    inline_keyboard_builder.button(
        text="Список админов", callback_data="all_admins"
    )

    inline_keyboard_builder.button(
        text="Назад", callback_data="back"
    )

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()

