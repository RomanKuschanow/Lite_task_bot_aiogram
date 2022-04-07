from aiogram.types import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from bot.keyboards.default.set_menu import set_menu
from bot.keyboards.inline import get_inline_states_markup
from bot.states.admins import ChangeStatus
from loader import dp, _, bot
from services.user import update_status, get_user


@dp.message_handler(commands='change_user_status', is_admin=True)
async def change_status(message: Message, state):
    bot_message = await message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, bot_message.message_id)

    text = _("Введи id пользователя")

    await ChangeStatus.user_id.set()

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))

    async with state.proxy() as data:
        data['message'] = list()
        data['message'].append(message.message_id)
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=ChangeStatus.user_id, menu=False)
async def get_id(message: Message, session, state, user):
    if not message.text.isnumeric():
        text = _("Мне нужен набор цифр")
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

        await message.answer(_("Статус изменен, id: {id}").format(id=message.text),
                             reply_markup=set_menu(user))

    await state.finish()
