from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Управление каналами", callback_data="control_channel")

    return inline_keyboard_builder.as_markup()


# control_channel
def control_channel_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Список каналов, откуда берутся посты", callback_data="out_channel")
    inline_keyboard_builder.button(text="Список каналов, куда заливаются посты", callback_data="in_channel")
    inline_keyboard_builder.button(text="Назад", callback_data="back")

    inline_keyboard_builder.adjust(1)

    return inline_keyboard_builder.as_markup()


def out_channel_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Добавить канал в список", callback_data="add_out_channel")
    inline_keyboard_builder.button(text="Удалить канал из списка", callback_data="delete_out_channel")
    inline_keyboard_builder.button(text="Назад", callback_data="control_channel")

    inline_keyboard_builder.adjust(2, 1)

    return inline_keyboard_builder.as_markup()


def in_channel_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()

    inline_keyboard_builder.button(text="Добавить канал в список", callback_data="add_in_channel")
    inline_keyboard_builder.button(text="Удалить канал из списка", callback_data="delete_in_channel")

    return inline_keyboard_builder.as_markup()
