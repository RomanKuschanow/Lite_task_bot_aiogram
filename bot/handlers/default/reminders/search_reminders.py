from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession
import re

from bot.keyboards.inline import get_reminders_list_inline_markup
from loader import dp, _
from models import User
from services.reminder import get_all_by_user_id, get_all_actual_by_user_id, get_all_old_by_user_id
from utils.misc import rate_limit
from .reminders_list import get_list

search_callback = CallbackData("reminder", "search", "action")
cancel_callback = CallbackData("reminder", "search", "cancle", "list", "mode", "page")


@dp.callback_query_handler(cancel_callback.filter())
async def cancel(callback_query: CallbackQuery, callback_data: dict, session: AsyncSession, user: User):
    await callback_query.answer()

    if callback_data["list"] == "all":
        function = get_all_by_user_id
    elif callback_data["list"] == "old":
        function = get_all_old_by_user_id
    else:
        function = get_all_actual_by_user_id

    text = await get_list(function, callback_data["mode"] == "view", session, user.id, int(callback_data["page"]))

    if text == "":
        text = _("У вас нет напоминаний в этой категории")

    max_page = int(len(await function(session, user.id)) / 25) + 1
    await callback_query.message.edit_text(text, reply_markup=get_reminders_list_inline_markup(callback_data["list"],
                                                                                               callback_data[
                                                                                                   "mode"] == "view",
                                                                                               int(callback_data[
                                                                                                       "page"]),
                                                                                               max_page))


# @dp.callback_query_handler(search_callback.filter())
# async def action(callback_query: CallbackQuery, callback_data: dict, session: AsyncSession, user: User):
#     if callback_data['action'] == 'text':


