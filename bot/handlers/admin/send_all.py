from aiogram.types import Message, ContentTypes
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from bot.keyboards.inline import get_inline_states_markup
from bot.keyboards.default.set_menu import set_menu

from loader import dp, _, bot
from bot.states.admins import AddAdmin
from services.user import update_is_admin, get_user

from bot.states.admins.sender import Sender

from scheduler import sender
from threading import Thread


@dp.message_handler(commands="send_all", is_admin=True)
async def _sender(message: Message, state):
    bot_message = await message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, bot_message.message_id)

    text = _("Введи текст")

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))

    await Sender.text_all.set()

    async with state.proxy() as data:
        data['message'] = list()
        data['message'].append(message.message_id)
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=Sender.text_all, content_types=ContentTypes.ANY, menu=False)
async def get_text(message: Message, state, user):
    if message.content_type != 'text':
        text = _('Ты прислал мне {type}, а нужно прислать текст').format(type=message.content_type)
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    t_s = Thread(target=sender, args=(message.text,))

    t_s.start()

    async with state.proxy() as data:
        data['message'].append(message.message_id)

        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

            await message.answer(_("Сообщение доставлено"), reply_markup=set_menu(user))

    await state.finish()

