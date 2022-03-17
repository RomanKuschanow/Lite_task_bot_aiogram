from aiogram.types import Message, CallbackQuery, ContentTypes
from aiogram.dispatcher.filters import Command
from bot.states import NewReminder
from sqlalchemy.ext.asyncio import AsyncSession
from utils.aiogram_calendar import simple_cal_callback, SimpleCalendar

from loader import dp, _, bot

from models import User

from bot.keyboards.inline import get_inline_cancle_markup
from datetime import datetime
from services.reminder import create_reminder
import re


@dp.message_handler(commands='new_reminder')
async def new_reminder(message: Message, state):
    text = _("Отправьте мне текст напоминания")

    bot_message = await message.answer(text, reply_markup=get_inline_cancle_markup())

    await NewReminder.text.set()

    async with state.proxy() as data:
        data['message'] = bot_message.message_id

    await message.delete()


@dp.message_handler(state=NewReminder.text, content_types=ContentTypes.ANY)
async def get_reminder_text(message: Message, state):
    if message.content_type != 'text':
        text = _(f'Вы прислали мне {message.content_type}, а нужно прислать текст')
        bot_message = await message.answer(text, reply_markup=get_inline_cancle_markup())
        async with state.proxy() as data:
            await bot.delete_message(message.chat.id, data['message'])
            data['message'] = bot_message.message_id
        await message.delete()
        return

    text = _("Теперь выберите дату")

    async with state.proxy() as data:
        data['text'] = message.text

    await NewReminder.date.set()

    bot_message = await message.answer(text, reply_markup=await SimpleCalendar().start_calendar())

    async with state.proxy() as data:
        await bot.delete_message(message.chat.id, data['message'])
        data['message'] = bot_message.message_id
    await message.delete()


@dp.callback_query_handler(simple_cal_callback.filter(), state=NewReminder.date)
async def get_reminder_date(callback_query: CallbackQuery, callback_data: dict, session, user, state):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:

        text = _("Отпраьте точное время")

        async with state.proxy() as data:
            data['date'] = date.strftime('%d.%m.%Y')

        await NewReminder.time.set()

        bot_message = await callback_query.message.answer(text, reply_markup=get_inline_cancle_markup())

        async with state.proxy() as data:
            data['message'] = bot_message.message_id
        await callback_query.message.delete()


@dp.message_handler(state=NewReminder.time, content_types=ContentTypes.ANY)
async def get_reminder_date(message, session, user, state):
    if message.content_type != 'text':
        text = _(f'Вы прислали мне {message.content_type}, а нужно прислать текст')
        bot_message = await message.answer(text, reply_markup=get_inline_cancle_markup())
        async with state.proxy() as data:
            await bot.delete_message(message.chat.id, data['message'])
            data['message'] = bot_message.message_id
        await message.delete()
        return

    if not re.match(r'^(\d{2})[\ |\:]?(\d{2})$', message.text):
        text = _('формат не соответсвует')
        bot_message = await message.answer(text, reply_markup=get_inline_cancle_markup())
        async with state.proxy() as data:
            await bot.delete_message(message.chat.id, data['message'])
            data['message'] = bot_message.message_id
        await message.delete()
        return

    text = ""

    match = re.search(r'^(\d{2})[\ |\:]?(\d{2})$', message.text)

    async with state.proxy() as data:
        await create_reminder(session, user.id, data['text'], datetime.strptime(f"{data['date']} {match[1]}:{match[2]}", '%d.%m.%Y %H:%M'))
        text = _(f"Напоминание '{data['text']}' установлено на {data['date']} {match[1]}:{match[2]}")
        await bot.delete_message(message.chat.id, data['message'])

    await message.answer(text)

    await message.delete()

    await state.finish()


@dp.message_handler(regexp='!(.+): (\d{2}\.\d{2}\.\d{4}\ \d{2}\:\d{2})')
async def new_reminder_via_regexp(message: Message, session: AsyncSession, user: User):
    match = re.search('!(.+): (\d{2}\.\d{2}\.\d{4}\ \d{2}\:\d{2})', message.text)
    reminder_text = match[1]
    date = datetime.strptime(match[2], '%d.%m.%Y %H:%M')

    text = (f'напоминание "{reminder_text}" установлено на {date.strftime("%d.%m.%Y %H:%M")}')

    create_reminder(user.id, reminder_text, date)

    await message.reply(  text)

