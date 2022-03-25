from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re

from loader import _


def get_reminders_search_inline_markup(back: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(InlineKeyboardButton(_("🔎 Искать по названию"), callback_data="reminder:search:text"),
               InlineKeyboardButton(_("🔎 Искать по дате"), callback_data="reminder:search:data"))
    markup.row(InlineKeyboardButton(_("⬅ Вернуться к списку"), callback_data=back))

    return markup

