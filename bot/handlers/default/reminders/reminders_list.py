from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession
import re

from bot.keyboards.inline import get_reminders_list_inline_markup, get_reminders_search_inline_markup
from loader import dp, _
from models import User
from services.reminder import get_all_by_user_id, get_all_actual_by_user_id, get_all_old_by_user_id
from utils.misc import rate_limit


list_callback = CallbackData('reminders', 'list', 'action')


@dp.message_handler(commands='reminders_list')
@rate_limit(3)
async def reminders_list(message: Message, session: AsyncSession, user: User):
    max_page = int(len(await get_all_by_user_id(session, user.id)) / 25) + 1

    text = await get_list(get_all_by_user_id, False, session, user.id, max_page)

    if text == "":
        text = _("У вас еще нет ни одного напоминания")

    await message.answer(text, reply_markup=get_reminders_list_inline_markup("all", curr_page=max_page, max_page=max_page))
    await message.delete()


@dp.callback_query_handler(list_callback.filter())
@rate_limit(3)
async def actual_reminders_list_callback(callback_query: CallbackQuery, callback_data: dict, session: AsyncSession,
                                         user: User):
    await callback_query.answer()
    function_list = {'all': get_all_by_user_id, 'old': get_all_old_by_user_id, 'actual': get_all_actual_by_user_id}

    keyboard = callback_query.message.reply_markup.inline_keyboard
    row = 1 if len(keyboard) == 3 else 0
    if row == 1:
        page = int(re.search('reminders:(\d+)', keyboard[1][1]['callback_data'])[1])
    else:
        page = 1

    max_page = int(len(await function_list[callback_data['list']](session, user.id)) / 25) + 1

    if callback_data["action"] != re.search('reminders:.+:(.+)', keyboard[row + 1][1]['callback_data'])[1]:
        page = max_page

    text = await get_list(function_list[callback_data['list']], callback_data['action'] == 'edit', session, user.id, page)

    if text == "":
        text = _("У вас нет напоминаний в этой категории")

    await callback_query.message.edit_text(text, reply_markup=get_reminders_list_inline_markup(callback_data['list'],
                                                                                          callback_data[
                                                                                              'action'] == 'edit',
                                                                                          curr_page=page,
                                                                                          max_page=max_page))


page_callback = CallbackData('reminders', 'page')


@dp.callback_query_handler(page_callback.filter())
@rate_limit(3)
async def page_select(callback_query: CallbackQuery, callback_data: dict, session: AsyncSession, user: User):
    await callback_query.answer()
    page = int(callback_data['page'])

    keyboard = callback_query.message.reply_markup.inline_keyboard

    if re.search('reminders:(.+):.+', keyboard[1][0]['callback_data'])[1] == "old" and \
            re.search('reminders:(.+):.+', keyboard[1][2]['callback_data'])[1] == "actual":
        function = get_all_by_user_id
        hidden_button = "all"
    elif re.search('reminders:(.+):.+', keyboard[1][0]['callback_data'])[1] == "all" and \
            re.search('reminders:(.+):.+', keyboard[1][2]['callback_data'])[1] == "actual":
        function = get_all_old_by_user_id
        hidden_button = "old"
    else:
        function = get_all_actual_by_user_id
        hidden_button = "actual"

    text = await get_list(function, re.search('reminders:.+:(.+)', keyboard[1][0]['callback_data'])[1] == "edit",
                          session, user.id, page)

    max_page = int(len(await function(session, user.id)) / 25) + 1
    await callback_query.message.edit_text(text, reply_markup=get_reminders_list_inline_markup(hidden_button,
                                                                                               re.search(
                                                                                                   'reminders:.+:(.+)',
                                                                                                   keyboard[1][0][
                                                                                                       'callback_data'])[
                                                                                                   1] == "edit",
                                                                                               curr_page=page,
                                                                                               max_page=max_page))


@dp.callback_query_handler(text='search')
@rate_limit(3)
async def search(callback_query: CallbackQuery, session: AsyncSession, user: User):
    await callback_query.answer()

    text = _("Выберите фильтр для поиска")

    keyboard = callback_query.message.reply_markup.inline_keyboard

    row = 1 if len(keyboard) == 3 else 0

    if re.search('reminders:(.+):.+', keyboard[row][0]['callback_data'])[1] == "old" and \
            re.search('reminders:(.+):.+', keyboard[row][2]['callback_data'])[1] == "actual":
        curr_list = "all"
    elif re.search('reminders:(.+):.+', keyboard[row][0]['callback_data'])[1] == "all" and \
            re.search('reminders:(.+):.+', keyboard[row][2]['callback_data'])[1] == "actual":
        curr_list = "old"
    else:
        curr_list = "actual"

    mode = "view" if re.search('reminders:.+:(.+)', keyboard[row][0]['callback_data'])[1] == "edit" else "edit"
    if row == 1:
        page = int(re.search('reminders:(\d+)', keyboard[1][1]['callback_data'])[1])
    else:
        page = 1

    await callback_query.message.edit_text(text, reply_markup=get_reminders_search_inline_markup(curr_list, mode, page))


async def get_list(function, is_edit, *parametrs) -> str:
    text = ""

    deep_link = "http://t.me/Lite_task_bot?start=edit_reminder_"

    reminders = list(await function(parametrs[0], parametrs[1])) if len(parametrs) == 3 else list(await function(parametrs[0], parametrs[1], parametrs[3], parametrs[4]))
    max_page = int(len(reminders) / 25) + 1

    for reminder in reminders if max_page == 1 else reminders[-25 * range(1, max_page + 1)[-parametrs[2]]:][:25]:
        text += f'{"✅" if reminder.is_reminded else "❌"} {reminder}' + (
            f'<a href="{deep_link}{reminder.id}">✏</a>\n' if is_edit else '\n')

    return text
