from aiogram import types
from aiogram.types import Message, CallbackQuery

from bot.keyboards.inline import get_timer_inline_markup
from data.config import BOT_NAME
from loader import dp, _
from models import User
from services.timer import get_all_actual_by_user_id


@dp.message_handler(commands="timer")
async def timer_menu(message: Message, user: User):
    text = await get_timers(user.id)

    await message.answer(text, reply_markup=get_timer_inline_markup(5, 10, 15, 20))


@dp.callback_query_handler(text_startswith="timer_list:update")
async def timer_menu_update(callback_query: CallbackQuery, user: User):
    text = await get_timers(user.id)

    await callback_query.message.edit_text(text, reply_markup=get_timer_inline_markup(5, 10, 15, 20),
                                           parse_mode=types.ParseMode.HTML)


async def get_timers(user_id: int) -> str:
    timers = get_all_actual_by_user_id(user_id)

    deep_link = f'http://t.me/{BOT_NAME}?start=edit_timer_'

    if len(timers) > 0:
        text = ""

        for timer in timers:
            text += f'{timer} <a href="{deep_link}{timer.id}">✏</a>\n'

        return text

    return _("У тебя нет активных таймеров")
