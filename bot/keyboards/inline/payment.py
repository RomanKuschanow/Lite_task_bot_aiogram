from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_payment_inline_markup(url: str, id: int):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Оплатить 💸', url=url))
    markup.add(InlineKeyboardButton('Оплатил ✅', callback_data=f'confirm_payment_{id}'))

    return markup
