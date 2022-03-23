from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession

from loader import dp, _
import re

from models import User
from services.reminder import get_all_by_user_id, get_all_actual_by_user_id, get_all_old_by_user_id
from bot.keyboards.inline import get_reminders_list_inline_markup
from .reminders_list import get_list
from utils.misc import rate_limit

page_callback = CallbackData('reminders', 'page')


@dp.callback_query_handler(page_callback.filter())
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
