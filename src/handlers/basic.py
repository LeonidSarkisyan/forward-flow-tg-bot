from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.entities.users.service import user_service
from src.keyboards.basic import main_keyboard, control_channel_keyboard, out_channel_keyboard


router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await user_service.add_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Привет, {message.from_user.first_name}! \n\n"
                         f"Я бот, который парсит другие каналы и сайты и может перенести контент"
                         f"в твои каналы!", reply_markup=main_keyboard())


F: CallbackQuery


@router.callback_query(F.data == "back")
async def back(call: CallbackQuery):
    await call.message.edit_reply_markup(
        reply_markup=main_keyboard()
    )


@router.callback_query(F.data == "control_channel")
async def send_channel_menu(call: CallbackQuery, bot: Bot):
    await call.message.edit_reply_markup(
        reply_markup=control_channel_keyboard()
    )
    #  await bot.copy_message(ADMIN_ID, message.chat.id, message.message_id)


@router.callback_query(F.data == "out_channel")
async def send_out_channel_menu(call: CallbackQuery):
    await call.message.edit_reply_markup(
        reply_markup=out_channel_keyboard()
    )


class LinkForm(StatesGroup):
    get_link = State()


@router.callback_query(F.data == "add_out_channel")
async def get_channel_link(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Отправьте пригласительную ссылку на канал типа: \n\n"
                              "https://t.me/example или example")
    await state.set_state(LinkForm.get_link)


@router.message(LinkForm.get_link)
async def send_channel_link(message: Message):
    if message.text:
        await message.answer("Чат добавлен!")
    else:
        pass
