from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re

from loader import _


def get_reminders_list_inline_markup(curr_list: str, is_edit: bool = False, curr_page: int = 1,
                                     max_page: int = 1) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    action = 'edit' if is_edit else 'view'

    tiles = [{'text': _("все"), 'callback': f"reminders:all:{curr_list}:{action}:{max_page}"},
             {'text': _("старые"), 'callback': f"reminders:old:{curr_list}:{action}:{max_page}"},
             {'text': _("предстоящие"), 'callback': f"reminders:actual:{curr_list}:{action}:{max_page}"}]

    for tile in range(3):
        if re.search("reminders:(.+):.+:.+:.+", tiles[tile - 1]['callback'])[1] == curr_list:
            tiles.pop(tile - 1)

    if max_page > 1:
        markup.row(
            InlineKeyboardButton('⬅', callback_data=f'reminders:{curr_list}:{curr_list}:{action}:{curr_page - 1 if curr_page > 1 else curr_page}'),
            InlineKeyboardButton(f'{curr_page}/{max_page}', callback_data='reminders:none'),
            InlineKeyboardButton('➡',
                                 callback_data=f'reminders:{curr_list}:{curr_list}:{action}:{curr_page + 1 if curr_page < max_page else curr_page}'))
    markup.row(InlineKeyboardButton(tiles[0]['text'], callback_data=f'{tiles[0]["callback"]}'),
               InlineKeyboardButton(_('🔄 Обновить'), callback_data=f'reminders:{curr_list}:{curr_list}:{action}:{curr_page}'),
               InlineKeyboardButton(tiles[1]['text'], callback_data=f'{tiles[1]["callback"]}'))
    markup.row(InlineKeyboardButton(_('🔎 Поиск'), callback_data='search'),
               InlineKeyboardButton(_('✏ Редактировать') if not is_edit else _('👀 Просмотр'),
                                    callback_data=f'reminders:{curr_list}:{curr_list}:edit:{curr_page}' if not is_edit else f'reminders:{curr_list}:{curr_list}:view:{curr_page}'))
    return markup
