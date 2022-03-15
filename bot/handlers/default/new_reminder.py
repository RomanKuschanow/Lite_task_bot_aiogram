from aiogram.types import Message
from bot.states import NewReminder
from sqlalchemy.ext.asyncio import AsyncSession

from loader import dp, _

from models import User

from datetime import datetime
from services.reminder import create_reminder
import re


@dp.message_handler(commands='new_reminder')
async def new_reminder(message: Message):
    text = _("Отправьте мне текст напоминания")

    await NewReminder.text.set()

    await message.reply(text)


@dp.message_handler(state=NewReminder.text)
async def get_reminder_text(message: Message, state):
    if message.content_type != 'text':
        text = _(f'Вы прислали мне {message.content_type}, а нужно прислать текст')
        return await message.reply(text)

    text = _("Теперь отправьте мне время в формате day.month.year hour:minute")

    async with state.proxy() as data:
        data['text'] = message.text

    await NewReminder.date.set()

    await message.reply(text)


@dp.message_handler(state=NewReminder.date)
async def get_reminder_date(message: Message, session: AsyncSession, state, user: User):
    if message.content_type != 'text':
        text = _(f'Вы прислали мне {message.content_type}, а нужно прислать текст')
        return await message.reply(text)

    if not re.match('(\d{2}\.\d{2}\.\d{4}\ \d{2}:\d{2})', message.text):
        text = _('формат не соответсвует')
        return await message.reply(text)

    text = _("напоминание успешно установлено")

    date = datetime.strptime(message.text, '%d.%m.%Y %H:%M')

    async with state.proxy() as data:
        await create_reminder(session, user.id, data['text'], date)

    await state.finish()

    await message.reply(text)


@dp.message_handler(regexp='!(.+): (\d{2}\.\d{2}\.\d{4}\ \d{2}\:\d{2})')
async def new_reminder_via_regexp(message: Message, session: AsyncSession, user: User):
    match = re.search('!(.+): (\d{2}\.\d{2}\.\d{4}\ \d{2}\:\d{2})', message.text)
    reminder_text = match[1]
    date = datetime.strptime(match[2], '%d.%m.%Y %H:%M')

    text = f'напоминание "{reminder_text}" установлено на {date.strftime("%d.%m.%Y %H:%M")}'

    create_reminder(user.id, reminder_text, date)

    await message.reply(  text)

