from aiogram.types.reply_keyboard import ReplyKeyboardMarkup

from loader import _


def get_admin_keyboard_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)

    markup.row(_("➕ Добавить Админа"), _("🎁 Выдать VIP"))
    markup.row(_("🔖 Рассылка"), _("📫 Личка"))
    markup.row(_("🔢 Количество пользователей"), _("🗂 Таблицы"))
    markup.row(_("🧾 Меню"))

    return markup

