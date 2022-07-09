from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_export_inline_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)

    markup.insert(InlineKeyboardButton('users', callback_data="export:users"))
    markup.insert(InlineKeyboardButton('reminders', callback_data="export:reminders"))

    return markup

