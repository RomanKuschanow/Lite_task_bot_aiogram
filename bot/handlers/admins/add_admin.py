from aiogram.types import Message
from bot.keyboards.inline import get_inline_states_markup

from loader import dp, _, bot
from bot.states.admins import AddAdmin
from services.user import update_is_admin, get_user


@dp.message_handler(commands='add_admin', is_admin=True)
async def add_admin(message: Message, state):
    text = _("Теперь введи id пользователя")

    await AddAdmin.user_id.set()

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))

    async with state.proxy() as data:
        data['message'] = list()
        data['message'].append(message.message_id)
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=AddAdmin.user_id)
async def get_id(message: Message, session, state):
    if not message.text.isnumeric():
        text = _("мне нужен набор цифр")
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    if await get_user(session, int(message.text)):
        await update_is_admin(session, int(message.text))

    async with state.proxy() as data:
        data['message'].append(message.message_id)
        for mes in data['message']:
            try:
                await bot.delete_message(message.chat.id, mes)
            except:
                continue

    await state.finish()

