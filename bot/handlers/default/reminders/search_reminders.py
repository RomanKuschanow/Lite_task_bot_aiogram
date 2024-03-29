import re
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentTypes
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from aiogram_datepicker import Datepicker

from bot.filters import vip
from bot.handlers.default.reminders.reminders_list import get_list
from bot.keyboards.default.set_menu import set_menu
from bot.keyboards.inline import get_inline_states_markup, get_reminders_list_inline_markup
from bot.states import SearchReminder
from loader import dp, _, bot
from models import User
from services.reminder import get_all_by_user_id, get_all_actual_by_user_id, get_all_old_by_user_id
from .datepicker_settings import _get_datepicker_settings

search_callback = CallbackData('reminder', 'search', 'filter')


@dp.callback_query_handler(search_callback.filter(), text_startswith="reminder:search")
@vip()
async def action(callback_query: CallbackQuery, callback_data: dict, user: User, state):
    bot_message = await callback_query.message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(callback_query.message.chat.id, bot_message.message_id)

    await callback_query.answer()

    keyboard = callback_query.message.reply_markup.inline_keyboard
    match = re.search('reminders:.+:(.+):(.+):(.+):.+:.*', keyboard[-1][0]['callback_data'])

    if callback_data['filter'] == 'text':
        text = _('Отправь мне текст для поиска')

        bot_message = await callback_query.message.answer(text, reply_markup=get_inline_states_markup(True))

        await SearchReminder.text.set()
        async with state.proxy() as data:
            data['list'] = match[1]
            data['mode'] = match[2]
            data['repeat_filter'] = match[3]
            data['message'] = list()
            data['message'].append(bot_message.message_id)
            data['main_message'] = callback_query.message.message_id

    if callback_data['filter'] == 'date':
        datepicker = Datepicker(_get_datepicker_settings(user.time_zone, True))
        markup = datepicker.start_calendar()
        text = _('Выбери дату')

        bot_message = await callback_query.message.answer(text, reply_markup=markup)

        await SearchReminder.date.set()
        async with state.proxy() as data:
            data['list'] = match[1]
            data['mode'] = match[2]
            data['repeat_filter'] = match[3]
            data['message'] = list()
            data['message'].append(bot_message.message_id)
            data['main_message'] = callback_query.message.message_id

    if callback_data['filter'] == 'time':
        text = _('Отправь точное время')

        bot_message = await callback_query.message.answer(text, reply_markup=get_inline_states_markup(True))

        await SearchReminder.time.set()
        async with state.proxy() as data:
            data['list'] = match[1]
            data['mode'] = match[2]
            data['repeat_filter'] = match[3]
            data['message'] = list()
            data['message'].append(bot_message.message_id)
            data['main_message'] = callback_query.message.message_id


@dp.message_handler(state=SearchReminder.text, content_types=ContentTypes.ANY, menu=False)
async def get_reminder_text(message: Message, state: FSMContext, user):
    if message.content_type != 'text':
        text = _('Ты прислал мне {type}, а нужно прислать текст').format(type=message.content_type)
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    async with state.proxy() as data:
        column = 'text'
        _filter = message.text

        function_list = {'all': get_all_by_user_id, 'old': get_all_old_by_user_id, 'actual': get_all_actual_by_user_id}

        text, max_page = get_list(function_list[data['list']], data['mode'] == 'edit', user.id, 0,
                                        column, _filter, data['repeat_filter'])

        await bot.edit_message_text(chat_id=user.id,
                                    message_id=data['main_message'],
                                    text=text,
                                    reply_markup=get_reminders_list_inline_markup(data['list'], data['mode'] == 'edit',
                                                                                  max_page, max_page,
                                                                                  data['repeat_filter'],
                                                                                  f'{column}:{_filter}'))

        data['message'].append(message.message_id)

        for mes in data['message']:
            try:
                await bot.delete_message(message.chat.id, mes)
            except:
                continue

    await message.answer(_("Напоминания отфильтрованы"), reply_markup=set_menu(user))

    await state.finish()


@dp.callback_query_handler(Datepicker.datepicker_callback.filter(), state=SearchReminder.date)
async def get_reminder_date(callback_query: CallbackQuery, callback_data: dict, user, state: FSMContext):
    await callback_query.answer()

    datepicker = Datepicker(_get_datepicker_settings(user.time_zone))
    date = await datepicker.process(callback_query, callback_data)
    if date:
        async with state.proxy() as data:
            data['date'] = datetime.strptime(f'{date.day}.{date.month}.{date.year}', '%d.%m.%Y').strftime('%d.%m.%Y')
    else:
        return

    async with state.proxy() as data:
        column = 'date'
        _filter = data['date']

        function_list = {'all': get_all_by_user_id, 'old': get_all_old_by_user_id, 'actual': get_all_actual_by_user_id}

        text, max_page = get_list(function_list[data['list']], data['mode'] == 'edit', user.id, 0,
                                        column, _filter, data['repeat_filter'])

        await bot.edit_message_text(chat_id=user.id,
                                    message_id=data['main_message'],
                                    text=text,
                                    reply_markup=get_reminders_list_inline_markup(data['list'], data['mode'] == 'edit',
                                                                                  max_page, max_page,
                                                                                  data['repeat_filter'],
                                                                                  f'{column}:{_filter}'))

        await bot.delete_message(callback_query.message.chat.id, data['message'][0])

    await state.finish()


@dp.message_handler(state=SearchReminder.time, content_types=ContentTypes.ANY, menu=False)
async def get_reminder_date(message, user, state: FSMContext):
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
        column = 'time'
        _filter = f'{match[1]}.{match[2]}'

        function_list = {'all': get_all_by_user_id, 'old': get_all_old_by_user_id,
                         'actual': get_all_actual_by_user_id}

        text, max_page = get_list(function_list[data['list']], data['mode'] == 'edit', user.id, 0,
                                        column, _filter, data['repeat_filter'])

        await bot.edit_message_text(chat_id=user.id,
                                    message_id=data['main_message'],
                                    text=text,
                                    reply_markup=get_reminders_list_inline_markup(data['list'],
                                                                                  data['mode'] == 'edit', max_page,
                                                                                  max_page,
                                                                                  data['repeat_filter'],
                                                                                  f'{column}:{_filter}'))

        data['message'].append(message.message_id)

        for mes in data['message']:
            try:
                await bot.delete_message(message.chat.id, mes)
            except:
                continue

    await message.answer(_("Напоминания отфильтрованы"), reply_markup=set_menu(user))

    await state.finish()
