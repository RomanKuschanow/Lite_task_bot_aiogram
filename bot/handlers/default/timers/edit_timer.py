from datetime import datetime
import re

from bot.filters import vip
from bot.keyboards.default.set_menu import set_menu
from bot.states import NewTimer
from loader import _, dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentTypes, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from bot.keyboards.inline import get_control_inline_markup, get_inline_states_markup
from models import User
from services.timer import get_timer, update_timer, pause, play

action_callback = CallbackData('timer', 'action', 'id')


@dp.callback_query_handler(action_callback.filter(), text_startswith="timer:update")
async def update_timer_menu(callback_query: CallbackQuery, callback_data: dict, user):
    timer = get_timer(int(callback_data["id"]), user.id)

    if timer:
        await callback_query.message.edit_text(f"{timer}", reply_markup=get_control_inline_markup(timer.id))
        return
    else:
        await callback_query.message.answer(_("Такого таймера не существует"))
        await callback_query.message.delete()
        return



@dp.message_handler(commands='start', text_startswith='/start edit_timer')
async def edit_timer_menu(message: Message, user):
    args = message.get_args()
    id = re.search('edit_timer_(\d+)', args)[1]

    timer = get_timer(int(id), user.id)

    if timer:
        await message.answer(f"{timer}", reply_markup=get_control_inline_markup(timer.id))
        await message.delete()
        return
    else:
        await message.answer(_("Такого таймера не существует"))
        return


@dp.callback_query_handler(action_callback.filter(), text_startswith="timer:delete")
async def delete_timer(callback_query: CallbackQuery, callback_data: dict, user):
    timer = get_timer(int(callback_data["id"]), user.id)

    update_timer(user.id, timer.id, is_work=False)
    await callback_query.message.answer(_("Таймер удален"), reply_markup=set_menu(user))
    await callback_query.message.delete()
    return


@dp.callback_query_handler(action_callback.filter(), text_startswith="timer:text")
async def edit_timer_text(callback_query: CallbackQuery, callback_data: dict, user, state):
    timer = get_timer(int(callback_data["id"]), user.id)

    if (timer.end_date - datetime.now()).total_seconds() >= 120:
        bot_message = await callback_query.message.answer("⁠", reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(callback_query.message.chat.id, bot_message.message_id)

        text = _("Отправь текст для таймера")

        await NewTimer.text.set()

        bot_message = await callback_query.message.answer(text, reply_markup=get_inline_states_markup(True))

        async with state.proxy() as data:
            data['main_message'] = callback_query.message.message_id
            data['message'] = list()
            data['message'].append(bot_message.message_id)
            data['id'] = timer.id

        return

    await callback_query.message.edit_text(f"{timer}", reply_markup=get_control_inline_markup(timer.id))
    await callback_query.message.answer(_("Нельзя редактировать время у таймера, до конца которого осталось меньше 2 минут"),
                                        reply_markup=set_menu(user))
    return


@dp.callback_query_handler(action_callback.filter(), text_startswith="timer:pause")
@vip()
async def pause_timer(callback_query: CallbackQuery, callback_data: dict, user):
    await callback_query.answer()

    timer = get_timer(int(callback_data["id"]), user.id)

    timer = pause(user.id, timer.id)
    await callback_query.message.edit_text(f"{timer}", reply_markup=get_control_inline_markup(timer.id))
    await callback_query.message.answer(_("Таймер остановлен"), reply_markup=set_menu(user))
    return


@dp.callback_query_handler(action_callback.filter(), text_startswith="timer:play")
@vip()
async def play_timer(callback_query: CallbackQuery, callback_data: dict, user):
    await callback_query.answer()

    timer = get_timer(int(callback_data["id"]), user.id)

    timer = play(user.id, timer.id)
    await callback_query.message.edit_text(f"{timer}", reply_markup=get_control_inline_markup(timer.id))
    await callback_query.message.answer(_("Таймер запущен"), reply_markup=set_menu(user))
    return


@dp.message_handler(state=NewTimer.text, content_types=ContentTypes.ANY, menu=False)
async def get_timer_text(message: Message, state: FSMContext, user: User):
    if message.content_type != 'text':
        text = _('Ты прислал мне {type}, а нужно прислать текст').format(type=message.content_type)
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    async with state.proxy() as data:
        update_timer(user.id, int(data['id']), text=message.text)

        await bot.edit_message_text(f"{get_timer(int(data['id']))}", chat_id=message.chat.id, message_id=data['main_message'],
                                    reply_markup=get_control_inline_markup(int(data['id'])))

        data['message'].append(message.message_id)

        await message.answer(_("Текст для таймера установлен"))

        for mes in data['message']:
            try:
                await bot.delete_message(message.chat.id, mes)
            except:
                continue

    await state.finish()
