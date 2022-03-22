from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline import get_reminders_list_inline_markup
from loader import dp, _
from models import User
from services.reminder import get_all_by_user_id, get_all_actual_by_user_id, get_all_old_by_user_id
from utils.misc import rate_limit


list_callback = CallbackData('reminders', 'list', 'action')


@dp.message_handler(commands='reminders_list')
@rate_limit(5)
async def reminders_list(message: Message, session: AsyncSession, user: User):
    text = _("У вас еще нет ни одного напоминания")

    max_page = int(len(await get_all_by_user_id(session, user.id)) / 25) + 1

    if await get_list(get_all_by_user_id, False, session, user.id, max_page) != "":
        text = await get_list(get_all_by_user_id, False, session, user.id, max_page)

    await message.answer(text, reply_markup=get_reminders_list_inline_markup("all", curr_page=max_page, max_page=max_page))
    await message.delete()


@dp.callback_query_handler(list_callback.filter())
@rate_limit(5)
async def actual_reminders_list_callback(callback_query: CallbackQuery, callback_data: dict, session: AsyncSession,
                                         user: User):
    function_list = {'all': get_all_by_user_id, 'old': get_all_old_by_user_id, 'actual': get_all_actual_by_user_id}

    text = _("У вас нет напоминаний в этой категории")

    max_page = int(len(await function_list[callback_data['list']](session, user.id)) / 25) + 1

    if await get_list(function_list[callback_data['list']], callback_data['action'] == 'edit', session, user.id,
                      max_page) != "":
        text = await get_list(function_list[callback_data['list']], callback_data['action'] == 'edit', session, user.id,
                              max_page)

    await callback_query.message.edit_text(text, reply_markup=get_reminders_list_inline_markup(callback_data['list'],
                                                                                          callback_data[
                                                                                              'action'] == 'edit',
                                                                                          curr_page=max_page,
                                                                                          max_page=max_page))


async def get_list(function, is_edit, *parametrs) -> str:
    text = ""

    deep_link = "http://t.me/Lite_task_bot?start=edit_reminder_"

    reminders = list(await function(parametrs[0], parametrs[1]))
    max_page = int(len(reminders) / 25) + 1

    for reminder in reminders if max_page == 1 else reminders[-25 * range(1, max_page + 1)[-parametrs[2]]:][:25]:
        text += f'{"✅" if reminder.is_reminded else "❌"} {reminder}' + (
            f'<a href="{deep_link}{reminder.id}">✏</a>\n' if is_edit else '\n')

    return text
