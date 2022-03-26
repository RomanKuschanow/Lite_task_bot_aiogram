from aiogram.types import Message
from utils.misc import rate_limit

from loader import dp, _


@dp.message_handler(commands="reset", state="*")
async def bot_start(message: Message, state):
    text = _("Действие прервано")

    async with state.proxy() as data:
        data['message'].append(message.message_id)
        async with state.proxy() as data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await message.answer(text)

    await state.finish()