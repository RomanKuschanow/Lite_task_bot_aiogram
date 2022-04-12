from aiogram.types import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from bot.filters import vip
from bot.keyboards.inline.reminders import get_reminders_repeat_inline_markup
from loader import dp, bot, _
from services.reminder import get_reminder, edit_repeating

repeat_callback = CallbackData('reminder', 'repeat', 'action', 'id')
repeat_question_callback = CallbackData('reminder_repeat', 'id')


@dp.callback_query_handler(repeat_question_callback.filter(), text_startswith="reminder_repeat")
@vip()
async def repaet_question(callback_query: CallbackQuery, callback_data, session, user):
    bot_message = await callback_query.message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(callback_query.message.chat.id, bot_message.message_id)

    await callback_query.answer()

    reminder = await get_reminder(session, int(callback_data['id']))

    text = _("{reminder}\n"
             "Повторение: {repeat}\n").format(reminder=reminder, repeat=_("Да") if reminder.is_repeat else _("Нет"))

    if reminder.is_repeat:
        if reminder.repeat_count:
            text += _("Количество повторений: {count}\n").format(
                count=reminder.repeat_count if reminder.repeat_count > 0 else _("Всегда"))

            if reminder.repeat_count > 0:
                _("Осталось: {left}\n").format(left=reminder.repeat_count - reminder.curr_repeat)

        elif reminder.repeat_until:
            text += _("Повторять до: {date}\n").format(date=reminder.repeat_until)

        text += _("Частота повторений: {range}").format(range=reminder.repeat_range)

    await callback_query.message.edit_text(text, reply_markup=get_reminders_repeat_inline_markup(reminder))


@dp.callback_query_handler(repeat_callback.filter(), text_startswith="reminder:repeat")
@vip()
async def repeat_enable(callback_query: CallbackQuery, callback_data, session, user):
    await callback_query.answer()

    await edit_repeating(session, callback_data['id'], user.id, callback_data['action'] == 'on')

    reminder = await get_reminder(session, int(callback_data['id']))

    text = _("{reminder}\n"
             "Повторение: {repeat}\n").format(reminder=reminder, repeat=_("Да") if reminder.is_repeat else _("Нет"))

    if reminder.is_repeat:
        if reminder.repeat_count:
            text += _("Количество повторений: {count}\n").format(
                count=reminder.repeat_count if reminder.repeat_count > 0 else _("Всегда"))

            if reminder.repeat_count > 0:
                _("Осталось: {left}\n").format(left=reminder.repeat_count - reminder.curr_repeat)

        elif reminder.repeat_until:
            text += _("Повторять до: {date}\n").format(date=reminder.repeat_until)

        text += _("Частота повторений: {range}").format(range=reminder.repeat_range)

    await callback_query.message.edit_text(text, reply_markup=get_reminders_repeat_inline_markup(reminder))
