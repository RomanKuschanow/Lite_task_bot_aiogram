from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_timer_inline_markup(*args) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5, resize_keyboard=True)

    for num in args:
        markup.insert(InlineKeyboardButton(f"{num}", callback_data=f"new_timer:{num}"))

    markup.row(InlineKeyboardButton(_("Другое время"), callback_data=f"new_timer:another"))

    markup.row(InlineKeyboardButton(_('🔄 Обновить'), callback_data="timer_list:update"))
    return markup

