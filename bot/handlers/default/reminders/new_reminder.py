import re
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentTypes
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram_datepicker import Datepicker
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import vip
from bot.keyboards.default.set_menu import set_menu
from bot.keyboards.inline import get_inline_states_markup
from bot.keyboards.inline import get_reminders_repeat_question_inline_markup
from bot.states import NewReminder
from loader import dp, _, bot
from models import User
from services.reminder import create_reminder
from utils.misc import rate_limit
from .datepicker_settings import _get_datepicker_settings


@dp.message_handler(commands='new_reminder')
@vip(5)
async def new_reminder(message: Message, state: FSMContext, session, user, call_from_back=False):
    bot_message = await message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, bot_message.message_id)

    text = _('Отправь мне текст напоминания')

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))

    await NewReminder.text.set()

    async with state.proxy() as data:
        if not call_from_back:
            data['message'] = list()
            data['fail'] = 0
            data['message'].append(message.message_id)
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=NewReminder.text, content_types=ContentTypes.ANY, menu=False)
async def get_reminder_text(message: Message, state: FSMContext, user, call_from_back=False):
    if message.content_type != 'text':
        text = _('Ты прислал мне {type}, а нужно прислать текст').format(type=message.content_type)
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['fail'] += 1
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    text = _('Теперь выбери дату')

    if not call_from_back:
        async with state.proxy() as data:
            data['text'] = message.text
            data['message'].append(message.message_id)
            for i in range(2 * data['fail']):
                await bot.delete_message(message.chat.id, data['message'][-2])
                data['message'].pop(-2)

            data['fail'] = 0

    await NewReminder.date.set()

    datepicker = Datepicker(_get_datepicker_settings(user.time_zone))
    markup = datepicker.start_calendar()

    bot_message = await message.answer(text, reply_markup=markup)

    async with state.proxy() as data:
        data['message'].append(bot_message.message_id)


@dp.callback_query_handler(Datepicker.datepicker_callback.filter(), state=NewReminder.date)
@rate_limit(3)
async def get_reminder_date(callback_query: CallbackQuery, callback_data: dict, session, user, state: FSMContext):
    await callback_query.answer()

    text = _('Отправь точное время')

    datepicker = Datepicker(_get_datepicker_settings(user.time_zone))
    date = await datepicker.process(callback_query, callback_data)
    if date:
        async with state.proxy() as data:
            data['date'] = f'{date.day}.{date.month}.{date.year}'
            await bot.edit_message_text(data['date'], callback_query.message.chat.id, callback_query.message.message_id)
    else:
        return

    await NewReminder.time.set()

    bot_message = await callback_query.message.answer(text, reply_markup=get_inline_states_markup())

    async with state.proxy() as data:
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=NewReminder.time, content_types=ContentTypes.ANY, menu=False)
async def get_reminder_date(message, session, user, state: FSMContext):
    if message.content_type != 'text':
        text = _('Ты прислал мне {type}, а нужно прислать текст').format(type=message.content_type)
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup())
        async with state.proxy() as data:
            data['fail'] += 1
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    if not re.match(r'^(\d{2})[\ |\:]?(\d{2})$', message.text):
        text = _('Формат не соответствует')
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup())
        async with state.proxy() as data:
            data['fail'] += 1
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    text = ""
    match = re.search(r'^(\d{2})[\ |\:]?(\d{2})$', message.text)

    async with state.proxy() as data:
        try:
            reminder = await create_reminder(session, user.id, data['text'],
                                             datetime.strptime(f'{data["date"]} {match[1]}:{match[2]}',
                                                               '%d.%m.%Y %H:%M'))
        except:
            text = _('Ты ввел несуществующее время')
            bot_message = await message.answer(text, reply_markup=get_inline_states_markup())
            async with state.proxy() as data:
                data['fail'] += 1
                data['message'].append(message.message_id)
                data['message'].append(bot_message.message_id)
            return
        text = _('Напоминание "{text}" установлено на {date} {hours}:{minutes}').format(text=data['text'],
                                                                                        date=data['date'],
                                                                                        hours=match[1],
                                                                                        minutes=match[2])
        data['message'].append(message.message_id)

    await message.answer(text, reply_markup=set_menu(user))
    await message.answer(_("Задать повторение для напоминания"),
                         reply_markup=get_reminders_repeat_question_inline_markup(reminder.id))

    async with state.proxy() as data:
        for mes in data['message']:
            try:
                await bot.delete_message(message.chat.id, mes)
            except:
                continue

    await state.finish()


@dp.callback_query_handler(text='back', state=[NewReminder.date, NewReminder.time])
async def back(callback_query: CallbackQuery, state: FSMContext, session, user):
    await callback_query.answer()
    async with state.proxy() as data:
        curr_state = data.state
    if curr_state == 'NewReminder:date':
        await NewReminder.time.set()
        await new_reminder(callback_query.message, state, session, user, True)
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

    text = _('Напоминание "{reminder_text}" установлено на {date}').format(reminder_text=reminder_text,
                                                                           date=date.strftime('%d.%m.%Y %H:%M'))

    await create_reminder(session, user.id, reminder_text, date)

    await message.reply(text, reply_markup=set_menu(user))
