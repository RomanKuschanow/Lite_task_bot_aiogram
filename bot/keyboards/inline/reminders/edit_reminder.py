from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import _


def get_edit_reminders_inline_markup(id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(InlineKeyboardButton(_('📝 Изменить название'), callback_data=f'reminder:edit:text:{id}'),
               InlineKeyboardButton(_('🗓 Изменить дату'), callback_data=f'reminder:edit:date:{id}'))
    markup.row(InlineKeyboardButton(_("⚙ Настроить повторение"), callback_data=f'reminder_repeat:{id}:1'))
    markup.row(InlineKeyboardButton(_('❎ Готово'), callback_data=f'done'),
               InlineKeyboardButton(_('🗑 Удалить напоминание'), callback_data=f'reminder:delete:{id}'))

    return markup
