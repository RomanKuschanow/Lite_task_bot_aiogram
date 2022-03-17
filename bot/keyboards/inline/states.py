from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_inline_states_markup(hidden_back: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(resize_keyboard = True)

    CANCEL = InlineKeyboardButton(_("❌ Отмена"), callback_data="search:cancel")
    BACK = InlineKeyboardButton(_("⬅ Назад"), callback_data="back")

    if hidden_back:
        markup.row(CANCEL)
    else:
        markup.row(BACK, CANCEL)

    return markup
