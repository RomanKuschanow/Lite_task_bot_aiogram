from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_payment_inline_markup(url: str, id: int):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(_('Оплатить 💸'), url=url))
    if id:
        markup.add(InlineKeyboardButton(_('Оплатил ✅'), callback_data=f'confirm_payment_{id}'))

    return markup
