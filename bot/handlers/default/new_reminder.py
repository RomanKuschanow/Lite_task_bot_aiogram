from aiogram.types import Message, CallbackQuery, ContentTypes
from aiogram.dispatcher.filters import Command
from bot.states import NewReminder
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from utils.aiogram_calendar import simple_cal_callback, SimpleCalendar

from loader import dp, _, bot

from models import User

from bot.keyboards.inline import get_inline_states_markup
from datetime import datetime
from services.reminder import create_reminder
import re


@dp.message_handler(commands='new_reminder')
async def new_reminder(message: Message, state: FSMContext, call_from_back = False):
    text = _("Отправьте мне текст напоминания")

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))

    await NewReminder.text.set()

    async with state.proxy() as data:
        if not call_from_back:
            data['message'] = list()
            data['fail'] = 0
            data['message'].append(message.message_id)
        data['message'].append(bot_message.message_id)
        print(data['message'])


@dp.message_handler(state=NewReminder.text, content_types=ContentTypes.ANY)
async def get_reminder_text(message: Message, state: FSMContext, call_from_back = False):
    if message.content_type != 'text':
        text = _(f'Вы прислали мне {message.content_type}, а нужно прислать текст')
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['fail'] += 1
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
            print(data['message'])
        return

    text = _("Теперь выберите дату")

    if not call_from_back:
        async with state.proxy() as data:
            data['text'] = message.text
            data['message'].append(message.message_id)
            for i in range(2 * data['fail']):
                await bot.delete_message(message.chat.id, data['message'][-2])
                data['message'].pop(-2)

            data['fail'] = 0
            print(data['message'])

    await NewReminder.date.set()

    bot_message = await message.answer(text, reply_markup=await SimpleCalendar().start_calendar())

    async with state.proxy() as data:
        data['message'].append(bot_message.message_id)
        print(data['message'])


@dp.callback_query_handler(simple_cal_callback.filter(), state=NewReminder.date)
async def get_reminder_date(callback_query: CallbackQuery, callback_data: dict, session, user, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:

        text = _("Отпраьте точное время")

        async with state.proxy() as data:
            data['date'] = date.strftime('%d.%m.%Y')

        await NewReminder.time.set()

        bot_message = await callback_query.message.answer(text, reply_markup=get_inline_states_markup())

        async with state.proxy() as data:
            data['message'].append(bot_message.message_id)
            print(data['message'])


@dp.message_handler(state=NewReminder.time, content_types=ContentTypes.ANY)
async def get_reminder_date(message, session, user, state: FSMContext):
    if message.content_type != 'text':
        text = _(f'Вы прислали мне {message.content_type}, а нужно прислать текст')
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup())
        async with state.proxy() as data:
            data['fail'] += 1
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
            print(data['message'])
        return

    if not re.match(r'^(\d{2})[\ |\:]?(\d{2})$', message.text):
        text = _('формат не соответсвует')
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup())
        async with state.proxy() as data:
            data['fail'] += 1
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
            print(data['message'])
        return

    text = ""

    match = re.search(r'^(\d{2})[\ |\:]?(\d{2})$', message.text)

    async with state.proxy() as data:
        try:
            await create_reminder(session, user.id, data['text'], datetime.strptime(f"{data['date']} {match[1]}:{match[2]}", '%d.%m.%Y %H:%M'))
        except:
            text = _('вы ввели несуществующее время')
            bot_message = await message.answer(text, reply_markup=get_inline_states_markup())
            async with state.proxy() as data:
                data['fail'] += 1
                data['message'].append(message.message_id)
                data['message'].append(bot_message.message_id)
                print(data['message'])
            return
        text = _(f"Напоминание '{data['text']}' установлено на {data['date']} {match[1]}:{match[2]}")
        data['message'].append(message.message_id)
        print(data['message'])

    await message.answer(text)

    async with state.proxy() as data:
        for mes in data['message']:
            try:
                await bot.delete_message(message.chat.id, mes)
            except:
                continue

    await state.finish()


@dp.callback_query_handler(text="back", state=[NewReminder.date, NewReminder.time])
async def back(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        curr_state = data.state
    if curr_state == 'NewReminder:date':
        await NewReminder.time.set()
        await new_reminder(callback_query.message, state, True)
        async with state.proxy() as data:
            for i in range(3):
                await bot.delete_message(callback_query.message.chat.id, data['message'][-2])
                data['message'].pop(-2)
    else:
        async with state.proxy() as data:
            for i in range(2 * (data['fail'] + 1)):
                await bot.delete_message(callback_query.message.chat.id, data['message'][-1])
                data['message'].pop()

            data['fail'] = 0
        await NewReminder.date.set()
        await get_reminder_text(callback_query.message, state, True)


@dp.message_handler(regexp='!(.+): (\d{2}\.\d{2}\.\d{4}\ \d{2}\:\d{2})')
async def new_reminder_via_regexp(message: Message, session: AsyncSession, user: User):
    match = re.search('!(.+): (\d{2}\.\d{2}\.\d{4}\ \d{2}\:\d{2})', message.text)
    reminder_text = match[1]
    date = datetime.strptime(match[2], '%d.%m.%Y %H:%M')

    text = (f'напоминание "{reminder_text}" установлено на {date.strftime("%d.%m.%Y %H:%M")}')

    create_reminder(user.id, reminder_text, date)

    await message.reply(  text)

