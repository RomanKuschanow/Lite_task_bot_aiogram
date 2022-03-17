from aiogram.types import Message, CallbackQuery

from loader import dp, _, bot


@dp.callback_query_handler(text='search:cancel', state="*")
async def bot_start(callback_query: CallbackQuery, state):
    text = _("Действие отменено")

    async with state.proxy() as data:
        await bot.delete_message(callback_query.message.chat.id, data['message'])

    await state.finish()

    await callback_query.message.answer(text)

    await callback_query.message.delete()
