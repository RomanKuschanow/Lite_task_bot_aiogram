from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from loader import dp, _


@dp.message_handler(CommandStart())
async def bot_start(message: Message, user):
    text = _("Привет, я Task Bot. Ты можешь составить список задачь, а я в назначенное время напомню тебе их сделать\n"
             "Пока что функционал у меня ограничен простыми напоминаниями, но в грядущих обновлениях мои возможности сильно увеличиться")

    await message.answer(text)

