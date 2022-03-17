from aiogram.types import Message, CallbackQuery

from loader import dp, _, bot


@dp.callback_query_handler(text='search:cancel', state="*")
async def bot_start(callback_query: CallbackQuery, state):
    text = _("Действие отменено")

    async with state.proxy() as data:
        data['message'].append(callback_query.message.message_id)
        async with state.proxy() as data:
            for mes in data['message']:
                try:
                    await bot.delete_message(callback_query.message.chat.id, mes)
                except:
                    continue

    await state.finish()

    await callback_query.message.answer(text)

    await callback_query.message.delete()
