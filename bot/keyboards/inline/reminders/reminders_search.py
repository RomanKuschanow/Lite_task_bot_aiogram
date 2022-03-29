from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import _


def get_reminders_search_inline_markup(back: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)

    markup.row(InlineKeyboardButton(_('📝 По названию'), callback_data=f'reminder:search:text::'),
               InlineKeyboardButton(_('📅 По дате'), callback_data=f'reminder:search:date::'),
               InlineKeyboardButton(_('⏰ По времени'), callback_data=f'reminder:search:time::'))
    markup.row(InlineKeyboardButton(_('🔎 Начать поиск'), callback_data=f'reminder:search:start::'))
    markup.row(InlineKeyboardButton(_('⬅ Вернуться к списку'), callback_data=back))

    return markup
