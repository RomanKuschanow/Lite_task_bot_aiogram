from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from loader import dp, _


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    text = _("Привет, я Task Bot. Я помогу тебе с планами на день, неделю, месяц.... жизнь =)\n" \
           "Если хочешь пройти небольшой экскурс по основным функциям, напиши /help, а для инфорамции о всех командах напиши /commands_list")

    await message.answer(text)

