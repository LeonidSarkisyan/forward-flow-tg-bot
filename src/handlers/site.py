from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from src.entities.site.site import SITES_URLS


router = Router()


@router.callback_query(F.data == 'control_site')
async def get_site_menu(call: CallbackQuery):
    await call.answer()
    site_list_string = "\n".join(SITES_URLS)
    await call.message.edit_text(
        "Вот список сайтов, с которых я беру информацию:\n\n"
        f"{site_list_string}",
        disable_web_page_preview=True
    )

