from aiogram.types import CallbackQuery

from loader import dp, _, bot

from bot.keyboards.default.set_menu import set_menu


@dp.callback_query_handler(text='done', state='*')
async def bot_start(callback_query: CallbackQuery, state, user):
    await callback_query.answer()
    text = _('Действие завершено')

    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(callback_query.message.chat.id, mes)
                except:
                    continue

    await callback_query.message.answer(text, reply_markup=set_menu(user))
    try:
        await callback_query.message.delete()
    except:
        pass
