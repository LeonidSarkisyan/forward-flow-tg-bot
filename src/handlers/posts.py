from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery

from src.entities.parsed_channels.service import parsed_channel_service
from src.entities.receiver_channels.service import receiver_channel_service
from src.keyboards.basic import after_added_in_channel_keyboard, add_more_out_channel_keyboard
from src.entities.setting.service import setting_service


router = Router()


F: Message


@router.channel_post(F.text.startswith("userbot__error__"))
async def error_by_add(message: Message, bot: Bot):
    error_type, user_id = message.text.split("__")[2:]
    if error_type == "invalid":
        await bot.send_message(
            user_id,
            "Некорректная ссылка  ❌\n\n"
            "Попробуйте ещё 👇👇👇",
            reply_markup=add_more_out_channel_keyboard()
        )
    elif error_type == "notfound":
        await bot.send_message(
            user_id,
            "Такой канал не найден  ❌\n\n"
            "Попробуйте ещё 👇👇👇",
            reply_markup=add_more_out_channel_keyboard()
        )


@router.channel_post(F.text.startswith("userbot__add__"))
async def get_and_add_channel_post(message: Message, bot: Bot):
    print("ПОЛУЧАЕМ!")
    channel_id, channel_username, user_id = message.text.split("__")[-3:]
    user_id = int(user_id)
    channel_id = int(channel_id)

    await parsed_channel_service.add_parsed_channel(channel_id, channel_username)
    await parsed_channel_service.bound_with_user(channel_id, channel_username, user_id)
    await bot.send_message(
        user_id,
        "Канал добавлен в \"Парсер список\"  ✅",
        reply_markup=add_more_out_channel_keyboard()
    )


@router.message(Command("new_receiver_channel"))
async def get_added_to_receiver_channel(message: Message):
    await message.answer("Чтобы я мог работать в вашем канале, сделайте следующее:\n\n"
                         "<b>1.</b> Добавить меня в ваш канал\n"
                         "<b>2.</b> Сделать меня администратором\n\n"
                         "После этих действий я отпишу вам, что всё прошло успешно.")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        event.from_user.id,
        f"Успешно! Вы добавили меня в <b>{event.chat.title}</b>!",
        reply_markup=after_added_in_channel_keyboard(event.chat.id)
    )
    await receiver_channel_service.add_receiver_channel(event.chat.id, event.chat.title, event.from_user.id)
    link = None
    if event.chat.username:
        link = f"https://t.me/{event.chat.username}"
    await setting_service.create_setting(
        event.chat.id, link
    )


@router.message(Command("delete_receiver_channel"))
async def get_added_to_receiver_channel(message: Message):
    await message.answer(
        "Чтобы я перестал отправлять посты в ваш канал, вы должны просто удалить меня от туда.\n\n"
        "Я сообщу вам сразу же после удаления."
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER))
async def bot_deleted(event: ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        event.from_user.id,
        f"Вы удалили меня из группы <b>{event.chat.title}</b>!"
    )
    await receiver_channel_service.delete_receiver_channel(event.chat.id)
