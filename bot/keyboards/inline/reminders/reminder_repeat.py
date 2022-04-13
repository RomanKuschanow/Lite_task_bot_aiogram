from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import _


def get_reminders_repeat_question_inline_markup(id: int, is_child: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)

    markup.row(InlineKeyboardButton(_("⚙ Настроить повторение"), callback_data=f'reminder_repeat:{id}:{int(is_child)}'))

    return markup


def get_reminders_repeat_inline_markup(reminder, is_child: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)

    if reminder.is_repeat:
        markup.row(InlineKeyboardButton(_("🚫 Отключить повторение"),
                                        callback_data=f"reminder:repeat:off:{reminder.id}:{int(is_child)}"))
        markup.row(InlineKeyboardButton(_("🔢 Количество"),
                                        callback_data=f"reminder:repeat:count:{reminder.id}:{int(is_child)}"),
                   InlineKeyboardButton(_("⏳ Повторять до"),
                                        callback_data=f"reminder:repeat:until:{reminder.id}:{int(is_child)}"))

        markup.row(
            InlineKeyboardButton(_("🔂 Частота"), callback_data=f"reminder:repeat:range:{reminder.id}:{int(is_child)}"))
    else:
        markup.row(InlineKeyboardButton(_("✅ Включить повторение"),
                                        callback_data=f"reminder:repeat:on:{reminder.id}:{int(is_child)}"))

    if is_child:
        markup.row(InlineKeyboardButton(_('⬅ Назад'), callback_data=f'back_to_edit:{reminder.id}'))
    else:
        markup.row(InlineKeyboardButton(_('❎ Готово'), callback_data=f'done'))

    return markup
