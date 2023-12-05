import json

from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.entities.setting.service import setting_service
from src.keyboards.processing import (
    get_menu_processing, with_setting, menu_link_keyboard, delete_word_keyboard, postscript_menu_keyboard
)


router = Router()


@router.callback_query(F.data.startswith("settings_in_channel__"))
async def open_setting_menu(call: CallbackQuery):
    receiver_channel_id = call.data.split("__")[-1]
    setting = await setting_service.get_settings(receiver_channel_id)
    print(setting)
    await call.message.edit_text(
        "Настройте обработку постов в канал, как вам захочется:",
        reply_markup=get_menu_processing(int(receiver_channel_id), setting)
    )


class LinkReceiverForm(StatesGroup):
    get_link_ = State()


@router.callback_query(F.data.startswith("menu_link__"))
async def link_menu(call: CallbackQuery, state: FSMContext):
    receiver_channel_id = call.data.split("__")[-1]
    setting = await setting_service.get_settings(receiver_channel_id)
    await call.message.edit_text(
        f"Ваша заменяющая ссылка: {setting.link}",
        reply_markup=menu_link_keyboard(int(receiver_channel_id), setting),
        disable_web_page_preview=True
    )
    await call.answer()


@router.callback_query(F.data.startswith("change_link__"))
async def ask_link(call: CallbackQuery, state: FSMContext):
    receiver_channel_id = call.data.split("__")[-1]
    await call.message.answer("Скиньте ссылку, на которую я буду заменять все ссылки в посте  👇👇👇")
    await state.set_state(LinkReceiverForm.get_link_)
    await state.update_data(receiver_channel_id=receiver_channel_id)


@router.message(LinkReceiverForm.get_link_, F.text)
async def get_link(message: Message, state: FSMContext):
    data = await state.get_data()
    await setting_service.add_link(message.text, data["receiver_channel_id"])
    await message.answer(
        "Ссылка добавлена успешно  ✅",
        reply_markup=with_setting(data["receiver_channel_id"])
    )
    await state.clear()


@router.callback_query(F.data.startswith("toggle_link__"))
async def toggle_link(call: CallbackQuery):
    receiver_channel_id = call.data.split("__")[-1]
    status = await setting_service.toggle_setting(receiver_channel_id)
    setting = await setting_service.get_settings(receiver_channel_id)
    await call.message.edit_text(
        f"Ваша заменяющая ссылка: {setting.link}",
        reply_markup=menu_link_keyboard(int(receiver_channel_id), status),
        disable_web_page_preview=True
    )
    if status:
        await call.answer("Автоподмена ссылки включена")
    else:
        await call.answer("Автоподмена ссылки выключена")


@router.callback_query(F.data.startswith("delete_word_posts__"))
async def menu_delete_words(call: CallbackQuery):
    receiver_channel_id = call.data.split("__")[-1]
    setting = await setting_service.get_settings(receiver_channel_id)
    try:
        deleted_words = setting.deleted_key_words.split("&&")
    except AttributeError:
        deleted_words = []
    print("Слова:", deleted_words)
    delete_string = ""
    if deleted_words != "null":
        index = 1
        for deleted_word in deleted_words:
            delete_string += f"<b>{index}.</b>  <code>{deleted_word}</code>\n"
            index += 1
    else:
        delete_string = "Вы пока не добавили никаких слов."
    await call.message.edit_text(
        "Ваши ключевые слова, которые удаляются из постов:\n\n"
        f"{delete_string}",
        reply_markup=delete_word_keyboard(int(receiver_channel_id))
    )


class DeleteWordForm(StatesGroup):
    get_add_words = State()
    get_delete_words = State()


@router.callback_query(F.data.startswith("add_delete_word__"))
async def ask_delete_word(call: CallbackQuery, state: FSMContext):
    receiver_channel_id = call.data.split("__")[-1]
    await call.message.answer(
        "Напишите слова (или фразы) через запятую и я добавлю их в список:"
    )
    await state.set_state(DeleteWordForm.get_add_words)
    await state.update_data(receiver_channel_id=receiver_channel_id)
    await call.answer()


@router.message(DeleteWordForm.get_add_words, F.text)
async def ask_delete_word(message: Message, state: FSMContext):
    data = await state.get_data()
    receiver_channel_id = data["receiver_channel_id"]
    words = message.text.split(",")
    words = [word.strip() for word in words]
    words = [word for word in words if len(word) > 0]
    words = await setting_service.add_words(words, receiver_channel_id)
    await message.answer("Слова добавлены успешно  ✅")

    delete_string = ""
    if words:
        index = 1
        for deleted_word in words:
            delete_string += f"<b>{index}.</b>  <code>{deleted_word}</code>\n"
            index += 1
    else:
        delete_string = "Вы пока не добавили никаких слов."
    await message.answer(
        "Ваши ключевые слова, которые удаляются из постов:\n\n"
        f"{delete_string}",
        reply_markup=delete_word_keyboard(int(receiver_channel_id))
    )


@router.callback_query(F.data.startswith("delete_delete_word__"))
async def ask_delete_del_word(call: CallbackQuery, state: FSMContext):
    receiver_channel_id = call.data.split("__")[-1]
    await call.message.answer(
        "Напишите слова (или фразы) через запятую и я удалю их из списка:"
    )
    await state.set_state(DeleteWordForm.get_delete_words)
    await state.update_data(receiver_channel_id=receiver_channel_id)
    await call.answer()


@router.message(DeleteWordForm.get_delete_words, F.text)
async def d_delete_word(message: Message, state: FSMContext):
    data = await state.get_data()
    receiver_channel_id = data["receiver_channel_id"]
    words = message.text.split(",")
    words = [word.strip() for word in words]
    words = [word for word in words if len(word) > 0]
    new_word = await setting_service.delete_words(words, receiver_channel_id)
    await message.answer("Слова удалены успешно  ✅")

    delete_string = ""
    if new_word:
        index = 1
        for deleted_word in new_word:
            delete_string += f"<b>{index}.</b>  <code>{deleted_word}</code>\n"
            index += 1
    else:
        delete_string = "Вы пока не добавили никаких слов."
    await message.answer(
        "Ваши ключевые слова, которые удаляются из постов:\n\n"
        f"{delete_string}",
        reply_markup=delete_word_keyboard(int(receiver_channel_id))
    )


@router.callback_query(F.data.startswith("postscript_post__"))
async def open_postscript_menu(call: CallbackQuery):
    receiver_channel_id = call.data.split("__")[-1]
    setting = await setting_service.get_settings(receiver_channel_id)
    postscript = setting.postscript if setting.postscript else 'Вы ещё не добавили подпись.'
    print(postscript)
    await call.message.answer(
        "Ваша подпись:\n\n"
        f"{postscript}",
        reply_markup=postscript_menu_keyboard(int(receiver_channel_id)),
        disable_web_page_preview=True
    )
    await call.answer()


class PostscriptForm(StatesGroup):
    get_postscript = State()


@router.callback_query(F.data.startswith("change_postscript__"))
async def ask_new_postscript(call: CallbackQuery, state: FSMContext):
    receiver_channel_id = call.data.split("__")[-1]
    await call.message.answer(
        "Напишите подпись, которая будет добавляться в конце поста. \n\n"
        "Рекомендуется отправить отформатированный текст, в который есть ссылка на ваш канал."
    )
    await state.set_state(PostscriptForm.get_postscript)
    await state.update_data(receiver_channel_id=receiver_channel_id)
    await call.answer()


@router.message(PostscriptForm.get_postscript)
async def get_postscript(message: Message, state: FSMContext):
    data = await state.get_data()
    receiver_channel_id = data["receiver_channel_id"]
    await setting_service.add_postscript(message.html_text, int(receiver_channel_id))
    await message.answer("Подпись была изменена  ✅")
    await state.clear()
    await message.answer(
        "Ваша подпись:\n\n"
        f"{message.html_text if message.html_text else 'Вы не добавили подпись'}",
        reply_markup=postscript_menu_keyboard(int(receiver_channel_id)),
        disable_web_page_preview=True
    )
