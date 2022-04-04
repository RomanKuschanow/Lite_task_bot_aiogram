from aiogram.types.reply_keyboard import ReplyKeyboardMarkup

from loader import _


def get_menu_keyboard_markup(is_admin: bool = False) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)

    markup.row(_("➕ Новое напоминание"), _("📝 Список напоминаний"))
    markup.row(_("💵 Донат"), _("❔ Помощь по командам"))
    if is_admin:
        markup.row(_("🛠 Админ-клавиатура"))

    return markup

