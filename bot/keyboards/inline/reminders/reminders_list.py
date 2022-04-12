import re

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import _


def get_reminders_list_inline_markup(curr_list: str, is_edit: bool = False, curr_page: int = 1,
                                     max_page: int = 1, repeat_filter: str = "all",
                                     search_filter: str = ':') -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    action = 'edit' if is_edit else 'view'

    tiles = [{'text': _('Все'),
              'callback': f'reminders:all:{curr_list}:{action}:{max_page}:{repeat_filter}:{search_filter}'},
             {'text': _('Старые'),
              'callback': f'reminders:old:{curr_list}:{action}:{max_page}:{repeat_filter}:{search_filter}'},
             {'text': _('Предстоящие'),
              'callback': f'reminders:actual:{curr_list}:{action}:{max_page}:{repeat_filter}:{search_filter}'}]

    for tile in range(3):
        if re.search('reminders:(.+):.+:.+:.+:.*:.*:.*', tiles[tile - 1]['callback'])[1] == curr_list:
            tiles.pop(tile - 1)

    if max_page > 1:
        markup.row(
            InlineKeyboardButton('⬅',
                                 callback_data=f'reminders:{curr_list}:{curr_list}:{action}:'
                                               f'{curr_page - 1 if curr_page > 1 else curr_page}:{repeat_filter}:{search_filter}'),
            InlineKeyboardButton(f'{curr_page}/{max_page}', callback_data='reminders:none'),
            InlineKeyboardButton('➡',
                                 callback_data=f'reminders:{curr_list}:{curr_list}:{action}:'
                                               f'{curr_page + 1 if curr_page < max_page else curr_page}'
                                               f':{repeat_filter}:{search_filter}'))
    markup.row(
        InlineKeyboardButton(tiles[0]['text'], callback_data=f'{tiles[0]["callback"]}'),
        InlineKeyboardButton(_('🔄 Обновить'),
                             callback_data=f'reminders:{curr_list}:{curr_list}:{action}:{curr_page}:{repeat_filter}:{search_filter}'),
        InlineKeyboardButton(tiles[1]['text'], callback_data=f'{tiles[1]["callback"]}'))

    markup.row(
        InlineKeyboardButton(_('🔎 Фильтры') if search_filter == ':' else _('❌ Сбросить фильтр'),
                             callback_data='search' if search_filter == ':'
                             else f'reminders:{curr_list}:{curr_list}:{action}:max:{repeat_filter}:{":"}'),

        InlineKeyboardButton(_('🔁 {tile}').format(tile=_("Только многоразовые") if repeat_filter == "all" else (
            _("Только одноразовые") if repeat_filter == "repeat" else _("Все"))),
                             callback_data=f'reminders:{curr_list}:{curr_list}:{action}:{curr_page}:'
                                           f'{"repeat" if repeat_filter == "all" else ("!repeat" if repeat_filter == "repeat" else "all")}:{search_filter}'),

        InlineKeyboardButton(_('✏ Редактировать') if not is_edit else _('👀 Просмотр'),
                             callback_data=f'reminders:{curr_list}:{curr_list}:edit:{curr_page}:{repeat_filter}:{search_filter}'
                             if not is_edit else f'reminders:{curr_list}:{curr_list}:view:{curr_page}:{repeat_filter}:{search_filter}'))
    return markup
