from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from bot.keyboards.inline import get_language_inline_markup
from loader import dp, _


@dp.message_handler(CommandStart())
async def bot_start(message: Message, user):
    text = _("Привет, я Task Bot. Ты можешь составить список задач, а я в назначенное время напомню тебе их сделать\n"
             "Пока что функционал у меня ограничен простыми напоминаниями, но в грядущих обновлениях мои возможности сильно увеличиться\n"
             "А теперь ты можешь выбрать свой язык, нажав на одну из кнопок ниже")

    await message.answer(text, reply_markup=get_language_inline_markup())

