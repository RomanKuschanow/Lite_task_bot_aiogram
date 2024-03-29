from aiogram.types import CallbackQuery, Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from aiogram_datepicker import Datepicker
from pendulum import datetime

from bot.filters import vip
from bot.keyboards.inline import get_reminders_repeat_inline_markup, get_num_inline_markup, get_range_inline_markup, \
    get_edit_reminders_inline_markup
from bot.states.default import EditRepeat
from loader import dp, bot, _
from services.reminder import get_reminder, edit_repeating, edit_freely
from utils import get_text
from utils.misc import rate_limit
from .datepicker_settings import _get_datepicker_settings

repeat_callback = CallbackData('reminder', 'repeat', 'action', 'id', 'is_child')
repeat_question_callback = CallbackData('reminder_repeat', 'id', 'is_child')


@dp.callback_query_handler(repeat_question_callback.filter(), text_startswith="reminder_repeat")
@vip()
async def repaet_question(callback_query: CallbackQuery, callback_data, user):
    bot_message = await callback_query.message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(callback_query.message.chat.id, bot_message.message_id)

    await callback_query.answer()

    reminder = get_reminder(int(callback_data['id']), user.id)

    await callback_query.message.edit_text(get_text(reminder),
                                           reply_markup=get_reminders_repeat_inline_markup(reminder, bool(
                                               int(callback_data['is_child']))))


@dp.callback_query_handler(repeat_callback.filter(), text_startswith="reminder:repeat")
async def repeat_enable(callback_query: CallbackQuery, callback_data, user, state):
    await callback_query.answer()

    id = int(callback_data['id'])

    if callback_data['action'] in ["on", "off"]:
        edit_repeating(id, user.id, callback_data['action'] == 'on')

    if callback_data['action'] == "count":
        await callback_query.message.edit_text(_("Отправьте число или выберите из предложенных ниже"),
                                               reply_markup=get_num_inline_markup(False, True, 5, 10, 15, 20, "inf"))
        await EditRepeat.count.set()

        async with state.proxy() as data:
            data['id'] = id
            data['is_child'] = bool(int(callback_data['is_child']))
            data['message'] = list()
            data['main'] = callback_query.message.message_id

        return

    if callback_data['action'] == "until":
        datepicker = Datepicker(_get_datepicker_settings(user.time_zone, False, True))
        markup = datepicker.start_calendar()

        await callback_query.message.edit_text(
            _("Выбери дату, до которой будет повторяться напоминание (не включительно)"), reply_markup=markup)
        async with state.proxy() as data:
            data['id'] = id
            data['is_child'] = bool(int(callback_data['is_child']))

        await EditRepeat.until.set()

        return

    if callback_data['action'] == "range":
        await callback_query.message.edit_text(_("Выберите промежуток для повторения напоминания"),
                                               reply_markup=get_range_inline_markup(False, is_admin=user.is_admin))

        await EditRepeat.range.set()

        async with state.proxy() as data:
            data['id'] = id
            data['is_child'] = bool(int(callback_data['is_child']))

        return

    reminder = get_reminder(id, user.id)

    await callback_query.message.edit_text(get_text(reminder),
                                           reply_markup=get_reminders_repeat_inline_markup(reminder, bool(
                                               int(callback_data['is_child']))))


num_callback = CallbackData("num", "number")


@dp.callback_query_handler(num_callback.filter(), state=EditRepeat.count, text_startswith="num")
async def get_count_callback(callback_query: CallbackQuery, callback_data, state, user):
    await callback_query.answer()

    async with state.proxy() as data:
        edit_freely(data['id'], user.id, repeat_count=int(callback_data['number']),
                          repeat_until=None)

        reminder = get_reminder(int(data['id']), user.id)

    await callback_query.message.edit_text(get_text(reminder),
                                           reply_markup=get_reminders_repeat_inline_markup(reminder, data['is_child']))

    await state.finish()


@dp.message_handler(state=EditRepeat.count, menu=False)
async def get_count_message(message: Message, state, user):
    num = message.text

    if not num.isnumeric() or int(num) < 1:
        bot_message = await message.answer(_('Введите целое число больше 0, например: 5'))
        async with state.proxy() as data:
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    async with state.proxy() as data:
        edit_freely(data['id'], user.id, repeat_count=int(num), repeat_until=None)

        reminder = get_reminder(int(data['id']), user.id)

    await bot.edit_message_text(get_text(reminder), message.chat.id, data['main'],
                                reply_markup=get_reminders_repeat_inline_markup(reminder, data['is_child']))

    async with state.proxy() as data:
        if 'message' in data:
            data['message'].append(message.message_id)
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()


@dp.callback_query_handler(Datepicker.datepicker_callback.filter(), state=EditRepeat.until)
@rate_limit(3)
async def get_until_date(callback_query: CallbackQuery, callback_data: dict, user, state):
    datepicker = Datepicker(_get_datepicker_settings(user.time_zone))
    date = await datepicker.process(callback_query, callback_data)
    date = datetime(date.year, date.month, date.day, 0, 0, tz=None)
    if date:
        async with state.proxy() as data:
            reminder = get_reminder(int(data['id']), user.id)
            if date < reminder.date:
                await callback_query.answer(_("Выбери дату которая больше начальной"))
                return

            edit_freely(data['id'], user.id, repeat_count=None,
                              repeat_until=datetime(date.year, date.month, date.day))

            await callback_query.message.edit_text(get_text(reminder),
                                                   reply_markup=get_reminders_repeat_inline_markup(reminder,
                                                                                                   data['is_child']))
    else:
        await callback_query.answer()
        return

    await state.finish()


range_callback = CallbackData("range", "name")


@dp.callback_query_handler(range_callback.filter(), state=EditRepeat.range, text_startswith="range")
async def get_range(callback_query: CallbackQuery, callback_data, user, state):
    await callback_query.answer()

    async with state.proxy() as data:
        edit_freely(data['id'], user.id, repeat_range=callback_data['name'])

        reminder = get_reminder(int(data['id']))

    await callback_query.message.edit_text(get_text(reminder),
                                           reply_markup=get_reminders_repeat_inline_markup(reminder, data['is_child']))

    await state.finish()


@dp.callback_query_handler(text='back', state=[EditRepeat.count, EditRepeat.until, EditRepeat.range])
async def back(callback_query: CallbackQuery, user, state):
    await callback_query.answer()

    async with state.proxy() as data:
        reminder = get_reminder(int(data['id']), user.id)

        await callback_query.message.edit_text(get_text(reminder),
                                               reply_markup=get_reminders_repeat_inline_markup(reminder,
                                                                                               data['is_child']))

        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()


back_to_edit_callback = CallbackData("back_to_edit", "id")


@dp.callback_query_handler(back_to_edit_callback.filter(), text_startswith='back_to_edit')
async def back_to_edit(callback_query: CallbackQuery, callback_data, user):
    await callback_query.answer()

    reminder = get_reminder(int(callback_data['id']), user.id)

    await callback_query.message.edit_text(get_text(reminder),
                                           reply_markup=get_edit_reminders_inline_markup(int(callback_data['id'])))
