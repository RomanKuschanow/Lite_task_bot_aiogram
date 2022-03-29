from aiogram.types import Message
from bot.keyboards.inline import get_inline_states_markup

from loader import dp, _, bot
from bot.states.admins import ChangeStatus
from services.user import update_status, get_user


@dp.message_handler(commands='change_user_status', is_admin=True)
async def change_status(message: Message, state):
    text = _("Теперь введи id пользователя")

    await ChangeStatus.user_id.set()

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))

    async with state.proxy() as data:
        data['message'] = list()
        data['message'].append(message.message_id)
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=ChangeStatus.user_id)
async def get_id(message: Message, session, state):
    if not message.text.isnumeric():
        text = _("мне нужен набор цифр")
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    if await get_user(session, int(message.text)):
        await update_status(session, int(message.text))

    async with state.proxy() as data:
        data['message'].append(message.message_id)
        for mes in data['message']:
            try:
                await bot.delete_message(message.chat.id, mes)
            except:
                continue

    await state.finish()

