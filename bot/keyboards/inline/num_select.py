from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_num_inline_markup(hidden_back: bool = True, hidden_cancel: bool = True, *args) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5, resize_keyboard=True)

    for num in args:
        if num == "inf":
            markup.insert(InlineKeyboardButton("♾", callback_data=f"num:{-1}"))
            continue
        markup.insert(InlineKeyboardButton(f"{num}", callback_data=f"num:{num}"))

    markup.row()

    CANCEL = InlineKeyboardButton(_('❌ Отмена'), callback_data='cancel')
    BACK = InlineKeyboardButton(_('⬅ Назад'), callback_data='back')

    if not hidden_back:
        markup.insert(BACK)
    if not hidden_cancel:
        markup.insert(CANCEL)

    return markup

