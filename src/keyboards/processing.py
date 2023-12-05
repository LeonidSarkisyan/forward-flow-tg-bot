from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_menu_processing(receiver_channel_id: int, settings):
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(
        text="Автоподмена ссылки в постах на свои",
        callback_data=f"menu_link__{receiver_channel_id}"
    )
    inline_keyboard_builder.button(
        text="Настроить удаляемые слова из постов",
        callback_data=f"delete_word_posts__{receiver_channel_id}"
    )
    inline_keyboard_builder.button(
        text="Настроить приписку в конце поста",
        callback_data=f"postscript_post__{receiver_channel_id}"
    )
    inline_keyboard_builder.button(
        text="Назад",
        callback_data=f"control_in_channel__{receiver_channel_id}"
    )

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


def menu_link_keyboard(receiver_channel_id: int, status):
    inline_keyboard_builder = InlineKeyboardBuilder()

    status = "🟢" if status else "🔴"

    inline_keyboard_builder.button(
        text="Поменять ссылку",
        callback_data=f"change_link__{receiver_channel_id}"
    )

    inline_keyboard_builder.button(
        text=f"Подмена ссылки  {status}",
        callback_data=f"toggle_link__{receiver_channel_id}"
    )

    inline_keyboard_builder.button(
        text="Назад",
        callback_data=f"settings_in_channel__{receiver_channel_id}"
    )

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


def with_setting(receiver_channel_id: int):
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(
        text="К настройкам",
        callback_data=f"settings_in_channel__{receiver_channel_id}"
    )

    return inline_keyboard_builder.as_markup()


def delete_word_keyboard(receiver_channel_id: int):
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(
        text="Добавить",
        callback_data=f"add_delete_word__{receiver_channel_id}"
    )

    inline_keyboard_builder.button(
        text="Удалить",
        callback_data=f"delete_delete_word__{receiver_channel_id}"
    )

    inline_keyboard_builder.button(
        text="Назад",
        callback_data=f"settings_in_channel__{receiver_channel_id}"
    )

    inline_keyboard_builder.adjust(2, 1)

    return inline_keyboard_builder.as_markup()


def postscript_menu_keyboard(receiver_channel_id: int):
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(
        text="Изменить подпись",
        callback_data=f"change_postscript__{receiver_channel_id}"
    )

    inline_keyboard_builder.button(
        text="Назад",
        callback_data=f"settings_in_channel__{receiver_channel_id}"
    )

    inline_keyboard_builder.adjust(1, 1)

    return inline_keyboard_builder.as_markup()
