from aiogram.types import CallbackQuery

from loader import dp, _, bot


@dp.callback_query_handler(text='cancel', state='*')
async def bot_start(callback_query: CallbackQuery, state):
    await callback_query.answer()
    text = _('Действие отменено')

    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(callback_query.message.chat.id, mes)
                except:
                    continue

    await state.finish()

    await callback_query.message.answer(text)
    await callback_query.message.delete()
