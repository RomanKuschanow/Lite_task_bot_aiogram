from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_inline_cancle_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(resize_keyboard = True)

    markup.row(InlineKeyboardButton(_("❌ Отмена"), callback_data="search:cancel"))

    return markup
