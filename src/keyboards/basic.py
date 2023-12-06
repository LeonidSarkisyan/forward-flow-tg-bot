from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard(role_id: int = 0):
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Управление каналами", callback_data="control_channel")

    if role_id == 1:
        inline_keyboard_builder.button(text="Управление админами", callback_data="control_admin")
        inline_keyboard_builder.button(text="Выйти из супер админа", callback_data="logout_super_admin")

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


# control_channel
def control_channel_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Список каналов, откуда берутся посты", callback_data="out_channel")
    inline_keyboard_builder.button(text="Список каналов, куда заливаются посты", callback_data="in_channel")
    inline_keyboard_builder.button(text="Назад", callback_data="back")

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


# out_channel
def out_channel_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Добавить", callback_data="add_out_channel")
    inline_keyboard_builder.button(text="Удалить", callback_data="delete_out_channel")
    inline_keyboard_builder.button(text="Назад", callback_data="control_channel")

    inline_keyboard_builder.adjust(2, 1)

    return inline_keyboard_builder.as_markup()


def add_more_out_channel_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Перейти в список", callback_data="out_channel")
    inline_keyboard_builder.button(text="Добавить ещё", callback_data="add_out_channel")

    return inline_keyboard_builder.as_markup()


# delete_out_channel
def delete_list_channels_keyboard(usernames: list[str]):
    inline_keyboard_builder = InlineKeyboardBuilder()

    for username in usernames:
        inline_keyboard_builder.button(text=f"@{username}", callback_data=f"delete_out__{username}")
    inline_keyboard_builder.button(text="Назад", callback_data="out_channel")

    count_usernames = len(usernames)

    sizes = (2 for i in range(count_usernames // 2))

    inline_keyboard_builder.adjust(*sizes, 1, repeat=True)

    return inline_keyboard_builder.as_markup()


# in_channel
def in_channel_keyboard(titles: list[str], ids: list[int]):
    inline_keyboard_builder = InlineKeyboardBuilder()

    for title, channel_id in zip(titles, ids):
        inline_keyboard_builder.button(text=title, callback_data=f"control_in_channel__{channel_id}")

    inline_keyboard_builder.button(text="Назад", callback_data="control_channel")

    inline_keyboard_builder.adjust(1, repeat=True)

    return inline_keyboard_builder.as_markup()


def after_added_in_channel_keyboard(chat_id: int):
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(
        text="Настроить мой канал",
        callback_data=f"control_in_channel__{chat_id}"
    )
    inline_keyboard_builder.button(
        text="Управление каналами", callback_data="control_channel"
    )

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


#  control_in_channel__
def menu_receive_channel_keyboard(receive_channel_id: int):
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(
        text="Настроить подключенные каналы", callback_data=f"list_out_channels__{receive_channel_id}"
    )
    inline_keyboard_builder.button(
        text="Настроить обработку постов",
        callback_data=f"settings_in_channel__{receive_channel_id}"
    )
    inline_keyboard_builder.button(text="Назад", callback_data="in_channel")

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


#  list_out_channels__
def list_out_channel_keyboard(flow: list, parsed_channels: list, receiver_channel_id: int):
    inline_keyboard_builder = InlineKeyboardBuilder()
    flow_ids = [flow_item.parsed_channel_id for flow_item in flow]

    for parsed_channel in parsed_channels:
        emoji = "🟢" if parsed_channel.id in flow_ids else "🔴"
        inline_keyboard_builder.button(
            text=f"@{parsed_channel.username} {emoji}",
            callback_data=f"toggle_flow__{parsed_channel.id}__{receiver_channel_id}"
        )

    if len(parsed_channels) == 0:
        inline_keyboard_builder.button(
            text="У вас нет каналов из \"Парсер списка\" (добавить)",
            callback_data="add_out_channel"
        )

    inline_keyboard_builder.button(text="Назад", callback_data=f"control_in_channel__{receiver_channel_id}")

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()
