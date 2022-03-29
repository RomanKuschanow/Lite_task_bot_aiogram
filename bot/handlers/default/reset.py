from aiogram.types import Message

from loader import dp, _


@dp.message_handler(commands='reset', state='*')
async def bot_start(message: Message, state):
    async with state.proxy() as data:
        if 'message' in data:
            data['message'].append(message.message_id)
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await message.answer(_('Действие прервано'))
    await state.finish()
