from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.config import POSTS_CHANNEL_ID
from src.entities.receiver_channels.service import receiver_channel_service
from src.entities.users.service import user_service
from src.keyboards.basic import (
    main_keyboard, control_channel_keyboard, in_channel_keyboard,
    out_channel_keyboard, delete_list_channels_keyboard, menu_receive_channel_keyboard,
    list_out_channel_keyboard, add_more_out_channel_keyboard
)
from src.entities.parsed_channels.service import parsed_channel_service
from src.entities.flow.service import flow_service


router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    user = await user_service.get_user(message.from_user.id)
    await message.answer(f"Привет, {message.from_user.first_name}! \n\n"
                         f"Я бот, который парсит другие каналы и сайты и может перенести контент "
                         f"в твои каналы!", reply_markup=main_keyboard(user.role_id))
    await state.clear()


F: CallbackQuery


@router.callback_query(F.data == "back")
async def back(call: CallbackQuery):
    user = await user_service.get_user(call.from_user.id)
    await call.message.edit_text(
        f"Привет, {call.from_user.first_name}! \n\n"
        f"Я бот, который парсит другие каналы и сайты и может перенести контент "
        f"в твои каналы!", reply_markup=main_keyboard(user.role_id)
    )


@router.callback_query(F.data == "control_channel")
async def send_channel_menu(call: CallbackQuery, bot: Bot):
    await call.message.edit_text(
        "Выберите список каналов:",
        reply_markup=control_channel_keyboard()
    )
    #  await bot.copy_message(ADMIN_ID, message.chat.id, message.message_id)


@router.callback_query(F.data == "out_channel")
async def send_out_channel_menu(call: CallbackQuery):
    await send_out_channel_menu_core(call)


@router.message(Command("parsed_channels"))
async def send_out_channel_menu(call: CallbackQuery):
    await send_out_channel_menu_core(call)


async def send_out_channel_menu_core(call: CallbackQuery | Message):
    usernames_channels = await parsed_channel_service.get_all_usernames(call.from_user.id)
    username_list = ""
    for username_channel in usernames_channels:
        username_list += f"@{username_channel} - <code>{username_channel}</code>\n"

    if isinstance(call, CallbackQuery):
        await call.message.edit_text(
            f"Ваш <b>\"Парсер список\"</b>: \n\n"
            f"{username_list}", reply_markup=out_channel_keyboard()
        )
    elif isinstance(call, Message):
        await call.answer(
            f"Ваш <b>\"Парсер список\"</b>: \n\n"
            f"{username_list}", reply_markup=out_channel_keyboard()
        )


class LinkForm(StatesGroup):
    get_link = State()
    get_usernames_for_delete = State()


@router.message(Command("new_parsed_channel"))
async def get_channel_link_for_command(message: Message, state: FSMContext):
    await message.answer(
        "Отправьте пригласительную ссылку на канал типа: \n\n"
        "<code>https://t.me/example</code> или <code>example</code>", disable_web_page_preview=True
    )
    await state.set_state(LinkForm.get_link)


@router.callback_query(F.data == "add_out_channel")
async def get_channel_link(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        "Отправьте пригласительную ссылку на канал типа: \n\n"
        "<code>https://t.me/example</code> или <code>example</code>", disable_web_page_preview=True
    )
    await state.set_state(LinkForm.get_link)


@router.message(Command("delete_parsed_channel"))
async def get_channel_link_for_delete(message: Message, state: FSMContext):
    usernames = await parsed_channel_service.get_all_usernames(message.from_user.id)
    await message.answer(
        "Кликните по каналу, который хотите удалить:",
        reply_markup=delete_list_channels_keyboard(usernames)
    )


@router.callback_query(F.data == "delete_out_channel")
async def get_channel_link_for_delete(call: CallbackQuery, state: FSMContext):
    await call.answer()
    usernames = await parsed_channel_service.get_all_usernames(call.from_user.id)
    await call.message.edit_text(
        "Кликните по каналу, который хотите удалить:",
        reply_markup=delete_list_channels_keyboard(usernames)
    )


@router.callback_query(F.data.startswith("delete_out_"))
async def delete_channel_from_user(call: CallbackQuery):
    username = call.data.split("__")[-1]
    await parsed_channel_service.delete_channel_for_user(username, call.from_user.id)
    usernames = await parsed_channel_service.get_all_usernames(call.from_user.id)
    await call.answer(f"Канал {username} удалён из \"Парсер списка\"")
    await call.message.edit_reply_markup(reply_markup=delete_list_channels_keyboard(usernames))


@router.message(LinkForm.get_link)
async def send_channel_link(message: Message, bot: Bot, state: FSMContext):
    if message.text:
        await bot.send_message(POSTS_CHANNEL_ID, f"bot__add__{message.text}__{message.from_user.id}")
        await state.clear()
    else:
        await message.answer("Отправьте ссылку типа: https://t.me/example или example")


@router.callback_query(F.data == "in_channel")
async def send_out_channel_menu(call: CallbackQuery):
    await send_in_channel_menu_core(call)


@router.message(Command("receiver_channels"))
async def send_out_channel_menu_with_message(message: Message):
    await send_in_channel_menu_core(message)


async def send_in_channel_menu_core(call: CallbackQuery | Message):
    receiver_channels = await receiver_channel_service.get_receiver_channels(call.from_user.id)
    titles = []
    ids = []
    for receiver_channel in receiver_channels:
        titles.append(receiver_channel.title)
        ids.append(receiver_channel.id)

    if isinstance(call, CallbackQuery):
        await call.message.edit_text(
            "Выберите канал из списка ниже:",
            reply_markup=in_channel_keyboard(titles, ids)
        )
    else:
        await call.answer(
            "Выберите канал из списка ниже:",
            reply_markup=in_channel_keyboard(titles, ids)
        )


@router.callback_query(F.data.startswith("control_in_channel__"))
async def go_to_receive_channel(call: CallbackQuery):
    receiver_channel_id = int(call.data.split("__")[-1])
    receiver_channel = await receiver_channel_service.get_receiver_channel(receiver_channel_id)
    await call.message.edit_text(
        f"Канал: <b>{receiver_channel.title}</b>\n\n"
        f"Что вы хотите сделать с ним?",
        reply_markup=menu_receive_channel_keyboard(receiver_channel_id)
    )


@router.callback_query(F.data.startswith("list_out_channels__"))
async def show_list_out_channel_by_receiver_channel_id(call: CallbackQuery):
    receiver_channel_id = int(call.data.split("__")[-1])
    parsed_channels = await parsed_channel_service.get_all_parsed_channels(call.from_user.id)
    flow = await flow_service.get_flow(receiver_channel_id)

    await call.message.edit_text(
        "Вы можете настроить, из каких каналов будут литься посты:\n\n"
        "Чтобы включить/выключить поток нужно кликуть по каналу.",
        reply_markup=list_out_channel_keyboard(flow, parsed_channels, receiver_channel_id)
    )


@router.callback_query(F.data.startswith("toggle_flow__"))
async def toggle_flow(call: CallbackQuery):
    parsed_channel_id, receiver_channel_id = call.data.split("__")[1:]
    if parsed_channel_id != receiver_channel_id:
        flow_station = await flow_service.toggle_flow(parsed_channel_id, receiver_channel_id)
        parsed_channels = await parsed_channel_service.get_all_parsed_channels(call.from_user.id)
        flow = await flow_service.get_flow(receiver_channel_id)
        await call.message.edit_text(
            "Вы можете настроить, из каких каналов будут литься посты:\n\n"
            "Чтобы включить/выключить поток нужно кликуть по каналу.",
            reply_markup=list_out_channel_keyboard(flow, parsed_channels, receiver_channel_id)
        )
        if flow_station:
            await call.answer("Поток включён")
        else:
            await call.answer("Поток выключен")
    else:
        await call.answer("Нельзя подключать канал к самому себе!")
