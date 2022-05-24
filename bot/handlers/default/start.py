from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from bot.keyboards.inline import get_language_inline_markup
from bot.states import Start
from loader import dp, _
import time

from aiogram.types import Message, WebAppInfo, MenuButtonWebApp


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    await Start.lang.set()

    text = _('Выберите свой язык')

    await message.answer(text, reply_markup=get_language_inline_markup())

    web_app_uri = 'https://lite-task-bot-aiogram.vercel.app/NewReminder'
    web_app_uri += '?time=' + str(time.time())

    await bot.set_chat_menu_button(message.chat.id, MenuButtonWebApp(text='+New', web_app=WebAppInfo(url=web_app_uri)))
