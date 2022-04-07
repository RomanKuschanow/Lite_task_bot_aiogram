import re
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentTypes
from aiogram.utils.callback_data import CallbackData
from aiogram_datepicker import Datepicker
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from bot.filters import vip
from bot.keyboards.inline import get_edit_reminders_inline_markup, get_inline_states_markup
from bot.keyboards.default.set_menu import set_menu
from bot.states.default.edit_reminder import EditReminder
from loader import dp, _, bot
from services.reminder import get_reminder, edit_text, edit_date, delete_reminder
from .datepicker_settings import _get_datepicker_settings
from bot.keyboards.default.set_menu import set_menu

edit_callback = CallbackData('reminder', 'edit', 'param', 'id')
delete_callback = CallbackData('reminder', 'delete', 'id')


@dp.message_handler(commands='start', text_startswith='/start edit_reminder')
async def edit_reminder_menu(message: Message, state: FSMContext, session, user):
    args = message.get_args()
    id = re.search('edit_reminder_(\d+)', args)[1]
    reminder = await get_reminder(session, int(id), user.id)

    if reminder:
        await message.answer(f'{"✅" if reminder.is_reminded else "❌"} {reminder}',
                             reply_markup=get_edit_reminders_inline_markup(id))
        await message.delete()


# @dp.callback_query_handler(text='reminder:edit:cancel')
# async def cancel_edit(callback_query: CallbackQuery):
#     await callback_query.answer()
#
#     await callback_query.message.delete()


@dp.callback_query_handler(delete_callback.filter())
async def del_reminder(callback_query: CallbackQuery, callback_data: dict, session, user):
    await callback_query.answer()

    await delete_reminder(session, user.id, int(callback_data['id']))
    await callback_query.message.answer(_("Напоминание удалено"), reply_markup=set_menu(user))
    await callback_query.message.delete()


@dp.callback_query_handler(edit_callback.filter())
@vip()
async def edit_reminder(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    bot_message = await callback_query.message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(callback_query.message.chat.id, bot_message.message_id)

    await callback_query.answer()

    if callback_data['param'] == 'text':
        text = _('Отправь мне текст напоминания')

        bot_message = await callback_query.message.answer(text, reply_markup=get_inline_states_markup(True))

        await EditReminder.text.set()

    elif callback_data['param'] == 'date':
        text = _('Выбери дату')

        datepicker = Datepicker(_get_datepicker_settings(True))
        markup = datepicker.start_calendar()

        bot_message = await callback_query.message.answer(text, reply_markup=markup)

        await EditReminder.date.set()

    async with state.proxy() as data:
        data['id'] = int(callback_data['id'])
        data['fail'] = 0
        data['message'] = list()
        data['message'].append(bot_message.message_id)
        data['main_message'] = callback_query.message.message_id


@dp.message_handler(state=EditReminder.text, content_types=ContentTypes.ANY, menu=False)
async def get_reminder_text(message: Message, state: FSMContext, session, user):
    if message.content_type != 'text':
        text = _('Ты прислал мне {type}, а нужно прислать текст').format(type=message.content_type)
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['fail'] += 1
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    async with state.proxy() as data:
        await edit_text(session, data['id'], message.text)

        reminder = await get_reminder(session, data['id'], user.id)
        await bot.edit_message_text(text=f'{"✅" if reminder.is_reminded else "❌"} {reminder}',
                                    reply_markup=get_edit_reminders_inline_markup(data['id']), chat_id=message.chat.id,
                                    message_id=data['main_message'])

        data['message'].append(message.message_id)

        for mes in data['message']:
            try:
                await bot.delete_message(message.chat.id, mes)
            except:
                continue

    await message.answer(_("Напоминание отредактировано"), reply_markup=set_menu(user))

    await state.finish()


date_reminders = CallbackData('datepicker', 'day', 'set-day', 'year', 'month', 'day')


@dp.callback_query_handler(Datepicker.datepicker_callback.filter(), date_reminders.filter(), state=EditReminder.date)
async def get_reminder_date(callback_query: CallbackQuery, callback_data: dict, session, user, state: FSMContext):
    await callback_query.answer()

    text = _('Отправь точное время')

    datepicker = Datepicker(_get_datepicker_settings())
    if callback_data['set-day'] == 'set-day':
        async with state.proxy() as data:
            data['date'] = f'{callback_data["day"]}.{callback_data["month"]}.{callback_data["year"]}'
            await bot.edit_message_text(data['date'], callback_query.message.chat.id, callback_query.message.message_id)
    else:
        return

    await EditReminder.time.set()

    bot_message = await callback_query.message.answer(text, reply_markup=get_inline_states_markup())

    async with state.proxy() as data:
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=EditReminder.time, content_types=ContentTypes.ANY, menu=False)
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

    match = re.search(r'^(\d{2})[\ |\:]?(\d{2})$', message.text)

    async with state.proxy() as data:
        try:
            await edit_date(session, data['id'], user.id,
                            datetime.strptime(f'{data["date"]} {match[1]}:{match[2]}', '%d.%m.%Y %H:%M'))
        except:
            text = _('Ты ввел несуществующее время')
            bot_message = await message.answer(text, reply_markup=get_inline_states_markup())
            async with state.proxy() as data:
                data['fail'] += 1
                data['message'].append(message.message_id)
                data['message'].append(bot_message.message_id)
            return

        reminder = await get_reminder(session, data['id'], user.id)
        await bot.edit_message_text(text=f'{"✅" if reminder.is_reminded else "❌"} {reminder}',
                                    reply_markup=get_edit_reminders_inline_markup(data['id']), chat_id=message.chat.id,
                                    message_id=data['main_message'])

        data['message'].append(message.message_id)

        for mes in data['message']:
            try:
                await bot.delete_message(message.chat.id, mes)
            except:
                continue

    await message.answer(_("Напоминание отредактировано"), reply_markup=set_menu(user))

    await state.finish()


@dp.callback_query_handler(text='back', state=EditReminder.time)
async def back(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    async with state.proxy() as data:
        for i in range(2 * (data['fail'] + 1)):
            await bot.delete_message(callback_query.message.chat.id, data['message'][-1])
            data['message'].pop()

        data['fail'] = 0
        await EditReminder.date.set()
        datepicker = Datepicker(_get_datepicker_settings(True))
        markup = datepicker.start_calendar()
        text = _('Выбери дату')

        bot_message = await callback_query.message.answer(text, reply_markup=markup)
        data['message'].append(bot_message.message_id)
