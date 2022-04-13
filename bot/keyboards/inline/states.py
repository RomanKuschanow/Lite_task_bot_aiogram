from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_inline_states_markup(hidden_back: bool = False, hidden_cancel: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(resize_keyboard=True)

    CANCEL = InlineKeyboardButton(_('❌ Отмена'), callback_data='cancel')
    BACK = InlineKeyboardButton(_('⬅ Назад'), callback_data='back')

    if not hidden_back:
        markup.insert(BACK)
    if not hidden_cancel:
        markup.insert(CANCEL)

    return markup
