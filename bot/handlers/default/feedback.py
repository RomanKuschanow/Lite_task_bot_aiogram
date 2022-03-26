from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message
from bot.keyboards.inline import get_inline_states_markup
from utils.misc import rate_limit
from bot.states import Feedback
from models import User

from loader import dp, _, bot


@dp.message_handler(commands='feedback')
async def feedback(message: Message, user, state):
    await Feedback.start.set()

    text = _("Напиши сообщение которое увидят разработчики")

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))

    async with state.proxy() as data:
        data['message'] = list()
        data['message'].append(bot_message.message_id)
        data['message'].append(message.message_id)


@dp.message_handler(state=Feedback.start)
async def forward(message: Message, user: User, state):
    text = f"{message.text} \n\n{user}"

    await bot.send_message(-1001588079833, text=text)

    async with state.proxy() as data:
        async with state.proxy() as data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()

