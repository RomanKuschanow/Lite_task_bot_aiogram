import re

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentTypes
from aiogram.utils.callback_data import CallbackData

from bot.filters import vip
from bot.keyboards.default.set_menu import set_menu
from bot.keyboards.inline import get_inline_states_markup, get_control_inline_markup
from bot.states import NewTimer
from loader import dp, bot, _
from models import User
from services.timer import create_timer

new_timer_callback = CallbackData("new_timer", "num")


@dp.callback_query_handler(new_timer_callback.filter(), text_startswith="new_timer:")
@vip(1, "timer")
async def new_timer(callback_query: CallbackQuery, callback_data: dict, user: User, state):
    await callback_query.answer()

    if callback_data['num'] == 'another':
        bot_message = await callback_query.message.answer("⁠", reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(callback_query.message.chat.id, bot_message.message_id)

        text = _("Отправь время для таймера")

        await NewTimer.time.set()

        bot_message = await callback_query.message.answer(text, reply_markup=get_inline_states_markup(True))

        async with state.proxy() as data:
            data['message'] = list()
            data['message'].append(bot_message.message_id)

        return
    else:
        timer = create_timer(user, int(callback_data['num']) * 60, _("Таймер"))
        await callback_query.message.answer(f'{timer}', reply_markup=get_control_inline_markup(timer.id))

        return


@dp.message_handler(state=NewTimer.time, content_types=ContentTypes.ANY, menu=False)
async def get_reminder_text(message: Message, state: FSMContext, user):
    if message.content_type != 'text':
        text = _('Ты прислал мне {type}, а нужно прислать текст').format(type=message.content_type)
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    if not re.match('(\d*):(\d{1,2}):?(\d{1,2})?|(\d*)', message.text):
        text = _('Формат не соответствует')
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    match = re.search('(\d*):(\d{1,2}):?(\d{1,2})?|(\d*)', message.text)

    if match[2] and int(match[2]) > 59:
        text = _('Минут в одном часе не может быть больше 59')
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    if match[3] and int(match[3]) > 59:
        text = _('Секунд в одной минуте не может быть больше 59')
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['fail'] += 1
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    if match[4]:
        time = int(match[4]) * 60
    else:
        if match[3]:
            time = int(match[1]) * 3600 + int(match[2]) * 60 + int(match[3])
        else:
            time = int(match[1]) * 3600 + int(match[2]) * 60

    await message.answer(_("Таймер запущен"), reply_markup=set_menu(user))

    timer = create_timer(user, time, _("Таймер"))
    await message.answer(f'{timer}', reply_markup=get_control_inline_markup(timer.id))

    async with state.proxy() as data:
        data['message'].append(message.message_id)
        for mes in data['message']:
            try:
                await bot.delete_message(message.chat.id, mes)
            except:
                continue

    await state.finish()

    return
