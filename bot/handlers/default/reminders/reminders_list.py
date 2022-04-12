import re

from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import vip
from bot.keyboards.inline import get_reminders_list_inline_markup, get_reminders_search_inline_markup
from loader import dp, _
from models import User
from services.reminder import get_all_by_user_id, get_all_actual_by_user_id, get_all_old_by_user_id
from utils.misc import rate_limit

from data.config import BOT_NAME

list_callback = CallbackData('reminders', 'list', 'curr_list', 'action', 'curr_page', 'repeat_filter', 'column', 'filter')


@dp.message_handler(commands='reminders_list')
@rate_limit(3)
async def reminders_list(message: Message, session: AsyncSession, user: User):
    text, max_page = await get_list(get_all_by_user_id, False, session, user.id, 0, 'all')

    if text == "":
        text = _('У вас еще нет ни одного напоминания')

    await message.answer(text,
                         reply_markup=get_reminders_list_inline_markup('all', curr_page=max_page, max_page=max_page))
    await message.delete()


@dp.callback_query_handler(list_callback.filter(), text_startswith="reminders")
@rate_limit(3)
async def actual_reminders_list_callback(callback_query: CallbackQuery, callback_data: dict, session: AsyncSession,
                                         user: User):
    await callback_query.answer()

    if callback_data['column']:
        column = callback_data['column']
        _filter = callback_data['filter']
        match_filter = f'{column}:{_filter}'
    else:
        match_filter = ':'

    function_list = {'all': get_all_by_user_id, 'old': get_all_old_by_user_id, 'actual': get_all_actual_by_user_id}

    page = int(callback_data['curr_page']) if callback_data['list'] == callback_data['curr_list'] \
                                              and callback_data['curr_page'] != 'max' else 0

    if match_filter == ':':
        text, max_page = await get_list(function_list[callback_data['list']], callback_data['action'] == 'edit',
                                        session, user.id, page, callback_data['repeat_filter'])
    else:
        text, max_page = await get_list(function_list[callback_data['list']], callback_data['action'] == 'edit',
                                        session, user.id, page, column, _filter, callback_data['repeat_filter'])

    page = int(callback_data['curr_page']) if callback_data['list'] == callback_data['curr_list'] \
                                              and callback_data['curr_page'] != 'max' else max_page

    if text == '':
        text = _('У вас нет напоминаний в этой категории')

    markup = get_reminders_list_inline_markup(callback_data['list'], callback_data['action'] == 'edit', curr_page=page,
                                              max_page=max_page, repeat_filter=callback_data['repeat_filter'], search_filter=match_filter)
    await callback_query.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(text='search')
@rate_limit(3)
@vip()
async def search(callback_query: CallbackQuery, session: AsyncSession, user: User):
    await callback_query.answer()

    text = _('Выберите фильтр')

    keyboard = callback_query.message.reply_markup.inline_keyboard

    await callback_query.message.edit_text(text, reply_markup=get_reminders_search_inline_markup(
        keyboard[-2][1]['callback_data']))


async def get_list(function, is_edit, session, user_id, *args) -> str:
    text = ""

    deep_link = f'http://t.me/{BOT_NAME}?start=edit_reminder_'

    reminders = list(await function(session, user_id))

    if args[-1] == "all":
        pass
    elif args[-1] == "repeat":
        reminders = [r for r in reminders if r.is_repeat]
    else:
        reminders = [r for r in reminders if not r.is_repeat]

    if len(args) == 4:
        if re.match(r'^(\d{2})\.(\d{2})$', args[2]):
            match = re.search(r'^(\d{2})\.(\d{2})$', args[2])
            _filter = f'{match[1]}:{match[2]}'
        else:
            _filter = args[2]

        text += f'Фильтр: {args[1]}: {_filter} \n'
        if args[1] == 'text':
            reminders = [r for r in reminders if re.match(_filter, r.text)]
        elif args[1] == 'date':
            reminders = [r for r in reminders if re.match(_filter, r.date.strftime('%d.%m.%Y'))]
        else:
            reminders = [r for r in reminders if re.match(_filter, r.date.strftime('%H:%M'))]

    max_page = int(len(reminders) / 25) + 1
    page = args[0] if args[0] > 0 else max_page

    for reminder in reminders if max_page == 1 else reminders[-25 * range(1, max_page + 1)[-page]:][:25]:
        text += f'{reminder}' + (
            f'<a href="{deep_link}{reminder.id}">✏</a>\n' if is_edit else '\n')

    if len(args) == 4:
        if text == f'Фильтр: {args[1]}: {_filter} \n':
            text += _('У вас еще нет ни одного напоминания c этим фильтром')

    return text, max_page
