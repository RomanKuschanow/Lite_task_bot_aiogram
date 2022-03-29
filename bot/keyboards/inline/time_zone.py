import re

import pytz
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _


def get_inline_tz_markup(region=None) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4, resize_keyboard=True)

    if region is None:
        buttons = list(set([re.search('(.+)/.+', r)[1] for r in pytz.all_timezones if re.match('(.+)/.+', r)]))
    else:
        buttons = list(set([re.search('.+/(.+)', r)[1] for r in pytz.all_timezones if re.match(region, r)]))

    buttons.sort()
    for button in range(len(buttons)):
        markup.insert(InlineKeyboardButton(buttons[button], callback_data=buttons[button]))

    CANCEL = InlineKeyboardButton(_('❌ Отмена'), callback_data='cancel')
    BACK = InlineKeyboardButton(_('⬅ Назад'), callback_data='back')

    if region is None:
        markup.row(CANCEL)
    else:
        markup.row(BACK, CANCEL)

    return markup
