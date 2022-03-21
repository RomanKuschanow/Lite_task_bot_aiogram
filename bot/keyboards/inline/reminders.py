from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re

from loader import _


def get_reminders_inline_markup(hidden_button: str, is_edit: bool = False, curr_page: int = 1, max_page: int = 1) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    action = 'edit' if is_edit else 'view'

    tiles = [{'text': _("все"), 'callback': f"reminders:all:{action}"},
             {'text': _("старые"), 'callback': f"reminders:old:{action}"},
             {'text': _("предстоящие"), 'callback': f"reminders:actual:{action}"}]

    for tile in range(3):
        if re.search("reminders:(.+):.+", tiles[tile - 1]['callback'])[1] == hidden_button:
            tiles.pop(tile - 1)

    if max_page > 1:
        markup.row(InlineKeyboardButton('⬅', callback_data=f'reminders:{curr_page - 1 if curr_page > 1 else curr_page}'),
                   InlineKeyboardButton(f'{curr_page}/{max_page}', callback_data='reminders:none'),
                   InlineKeyboardButton('➡', callback_data=f'reminders:{curr_page + 1 if curr_page < max_page else curr_page}'))
    markup.row(InlineKeyboardButton(tiles[0]['text'], callback_data=f'{tiles[0]["callback"]}'),
               InlineKeyboardButton(tiles[1]['text'], callback_data=f'{tiles[1]["callback"]}'))
    markup.row(InlineKeyboardButton(_('✏ Редактировать') if not is_edit else _('👀 Просмотр'),
                                    callback_data= f'reminders:{hidden_button}:edit' if not is_edit else f'reminders:{hidden_button}:view'))
    return markup
