from aiogram.types import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from bot.keyboards.default import get_menu_keyboard_markup
from bot.keyboards.inline import get_inline_states_markup
from bot.states.admins import AddAdmin
from loader import dp, _, bot
from services.user import update_is_admin, get_user


@dp.message_handler(commands='add_admin', is_admin=True)
async def add_admin(message: Message, state):
    bot_message = await message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, bot_message.message_id)

    text = _("Введи id пользователя")

    await AddAdmin.user_id.set()

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))

    async with state.proxy() as data:
        data['message'] = list()
        data['message'].append(message.message_id)
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=AddAdmin.user_id, menu=False)
async def get_id(message: Message, session, state, user):
    if not message.text.isnumeric():
        text = _("Мне нужен набор цифр")
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

        await message.answer(_("Админ добавлен, id: {id}").format(id=message.text),
                             reply_markup=(get_menu_keyboard_markup(user.is_admin)))

    await state.finish()
