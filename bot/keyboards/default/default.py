from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from loader import _


def set_default_markup(user):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(_('🆘 Помощь'))


    if user.is_admin:
        markup.row(_('📁 Экспорт пользователей'), _('📁 Экспорт пользователей'))

    return markup
