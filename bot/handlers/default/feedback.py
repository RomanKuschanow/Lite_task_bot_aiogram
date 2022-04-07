from aiogram.types import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from bot.keyboards.inline import get_inline_states_markup
from bot.keyboards.default.set_menu import set_menu
from bot.states import Feedback
from loader import dp, _, bot
from models import User

from data.config import FEED_BACK_CHANEL


@dp.message_handler(commands='feedback')
async def feedback(message: Message, user, state):
    bot_message = await message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, bot_message.message_id)

    await Feedback.start.set()

    text = _('Напиши сообщение которое увидят разработчики')

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))

    async with state.proxy() as data:
        data['message'] = list()
        data['message'].append(bot_message.message_id)
        data['message'].append(message.message_id)


@dp.message_handler(state=Feedback.start, menu=False)
async def forward(message: Message, user: User, state):
    text = f'{message.text} \n\n{user}'

    await bot.send_message(FEED_BACK_CHANEL, text=text)

    async with state.proxy() as data:
        async with state.proxy() as data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await message.answer(_("Спасибо. Мы получили твое сообщение"), reply_markup=set_menu(user))

    await state.finish()
