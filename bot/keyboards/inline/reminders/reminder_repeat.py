from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import _


def get_reminders_repeat_question_inline_markup(id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)

    markup.row(InlineKeyboardButton(_("⚙ Настроить повторение"), callback_data=f'reminder_repeat:{id}'))

    return markup


def get_reminders_repeat_inline_markup(reminder) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)

    if reminder.is_repeat:
        markup.row(InlineKeyboardButton(_("🚫 Отключить повторение"), callback_data=f"reminder:repeat:off:{reminder.id}"))
        markup.row(InlineKeyboardButton(_("🔢 Количество"), callback_data=f"reminder:repeat:count:{reminder.id}"),
                   InlineKeyboardButton(_("⏳ Повторять до"), callback_data=f"reminder:repeat:until:{reminder.id}"),
                   InlineKeyboardButton(_("🔂 Частота"), callback_data=f"reminder:repeat:range:{reminder.id}"),)
    else:
        markup.row(InlineKeyboardButton(_("✅ Включить повторение"), callback_data=f"reminder:repeat:on:{reminder.id}"))

    markup.row(InlineKeyboardButton(_('❎ Готово'), callback_data=f'done'))

    return markup

