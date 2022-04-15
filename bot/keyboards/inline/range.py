from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_range_inline_markup(hidden_back: bool = True, hidden_cancel: bool = True, is_admin: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5, resize_keyboard=True)

    markup.row()

    if is_admin:
        markup.insert(InlineKeyboardButton(_("⏰ Минута"), callback_data="range:min"))

    markup.insert(InlineKeyboardButton(_("📆 День"), callback_data="range:day"))
    markup.insert(InlineKeyboardButton(_("🗓 Неделя"), callback_data="range:week"))
    markup.insert(InlineKeyboardButton(_("🌙 Месяц"), callback_data="range:month"))
    markup.insert(InlineKeyboardButton(_("💫 Год"), callback_data="range:year"))

    markup.row()

    CANCEL = InlineKeyboardButton(_('❌ Отмена'), callback_data='cancel')
    BACK = InlineKeyboardButton(_('⬅ Назад'), callback_data='back')

    if not hidden_back:
        markup.insert(BACK)
    if not hidden_cancel:
        markup.insert(CANCEL)

    return markup

