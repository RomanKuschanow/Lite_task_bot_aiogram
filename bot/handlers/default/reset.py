from aiogram.types import Message

from loader import dp, _


@dp.message_handler(commands="reset", state="*")
async def bot_start(message: Message, state):
    text = _("Действие прервано")

    await message.answer(text)

    await state.finish()