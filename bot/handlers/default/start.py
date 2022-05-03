from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from bot.keyboards.inline import get_language_inline_markup
from bot.states import Start
from loader import dp, _


@dp.message_handler(CommandStart())
async def bot_start(message: Message):

    await Start.lang.set()

    text = _('Выберите свой язык')

    await message.answer(text, reply_markup=get_language_inline_markup())
