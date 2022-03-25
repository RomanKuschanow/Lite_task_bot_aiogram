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


# @dp.callback_query_handler(search_callback.filter())
# async def action(callback_query: CallbackQuery, callback_data: dict, session: AsyncSession, user: User):
#     if callback_data['action'] == 'text':


