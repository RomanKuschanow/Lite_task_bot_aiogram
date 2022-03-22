from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re

from loader import _


def get_edit_reminders_inline_markup(id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(InlineKeyboardButton(_("📝 Изменить название"), callback_data=f"reminder:edit:text:{id}"),
               InlineKeyboardButton(_("🗓 Изменить дату"), callback_data=f"reminder:edit:date:{id}"))
    markup.row(InlineKeyboardButton(_("❌ Отмена"), callback_data=f"reminder:edit:cancel"),
               InlineKeyboardButton(_("🗑 Удалить напоминание"), callback_data=f"reminder:delete:{id}"))

    return markup

