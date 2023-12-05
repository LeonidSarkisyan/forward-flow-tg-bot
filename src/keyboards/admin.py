from aiogram.utils.keyboard import InlineKeyboardBuilder


#  control_admin
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


#  all_admins
def admin_list_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(
        text="Удалить админа", callback_data="delete_admin_list"
    )

    inline_keyboard_builder.button(
        text="Назад", callback_data="control_admin"
    )

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


#  delete_admin_list
def admin_delete_list(admins):
    if not admins:
        admins = []

    inline_keyboard_builder = InlineKeyboardBuilder()

    for admin in admins:
        inline_keyboard_builder.button(
            text=f"@{admin.username}", callback_data=f"delete_admin_one__{admin.id}"
        )

    inline_keyboard_builder.button(
        text="Назад", callback_data="control_admin"
    )

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


