from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re

from loader import _


def get_reminders_search_inline_markup(list: str, mode: str, page: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(InlineKeyboardButton(_("🔎 Искать по названию"), callback_data="reminder:search:text"),
               InlineKeyboardButton(_("🔎 Искать по дате"), callback_data="reminder:search:data"))
    markup.row(InlineKeyboardButton(_("⬅ Вернуться к списку"), callback_data=f"reminder:search:cancle:{list}:{mode}:{page}"))

    return markup

