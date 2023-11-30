from aiogram.utils.keyboard import ReplyKeyboardBuilder


def send_channel():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text="Отправить канал", request_chat=True)
