from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_range_inline_markup(hidden_back: bool = True, hidden_cancel: bool = True) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4, resize_keyboard=True)

    markup.row(InlineKeyboardButton(_("📆 День"), callback_data="range:day"),
               InlineKeyboardButton(_("🗓 Неделя"), callback_data="range:week"),
               InlineKeyboardButton(_("🌙 Месяц"), callback_data="range:month"),
               InlineKeyboardButton(_("💫 Год"), callback_data="range:year"))

    markup.row()

    CANCEL = InlineKeyboardButton(_('❌ Отмена'), callback_data='cancel')
    BACK = InlineKeyboardButton(_('⬅ Назад'), callback_data='back')

    if not hidden_back:
        markup.insert(BACK)
    if not hidden_cancel:
        markup.insert(CANCEL)

    return markup

