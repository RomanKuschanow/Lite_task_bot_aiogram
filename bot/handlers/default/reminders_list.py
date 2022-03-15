from aiogram.types import Message
from bot.states import NewReminder
from sqlalchemy.ext.asyncio import AsyncSession

from loader import dp, _

from models import User

from datetime import datetime


@dp.message_handler(commands='reminders_list')
async def reminders_list(message: Message, session: AsyncSession, user: User):
    user_reminders =  await user.reminders

    text = f'{user_reminders}'

    await message.reply(text)

