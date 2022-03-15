from aiogram.types import Message, ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from loader import dp, _

from models import User
from services.reminder import get_all_by_user_id

from utils.misc.logging import logger

from datetime import datetime


@dp.message_handler(commands='reminders_list')
async def reminders_list(message: Message, session: AsyncSession, user: User):
    text = ""

    for reminder in await get_all_by_user_id(session, user.id):
        text += f'{reminder.text}: {reminder.date.strftime("%d.%m.%Y %H:%M")}\n'

    if text == "":
        text = "У вас еще нет ни одного напоминания"

    await message.reply(text)

