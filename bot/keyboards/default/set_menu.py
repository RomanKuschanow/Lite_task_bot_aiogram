from aiogram.types.reply_keyboard import ReplyKeyboardRemove, ReplyKeyboardMarkup

from models import User
from .admin import get_admin_keyboard_markup
from .menu import get_menu_keyboard_markup


def set_menu(user: User) -> ReplyKeyboardMarkup:
    settings = user.settings

    if settings.kb_enabled:
        if settings.last_kb == "main":
            return get_menu_keyboard_markup(user.is_admin)
        elif settings.last_kb == "admin":
            return get_admin_keyboard_markup()
    else:
        return ReplyKeyboardRemove()
