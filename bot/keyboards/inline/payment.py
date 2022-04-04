from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_payment_inline_markup(url: str):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(_('Оплатить 💸'), url=url))

    return markup
