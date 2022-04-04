from aiogram.types import Message, ContentTypes
from bot.keyboards.inline import get_inline_states_markup

from loader import dp, _, bot
from bot.states.admins import AddAdmin
from services.user import update_is_admin, get_user

from bot.states.admins.sender import Sender

from scheduler import between_callback, sender
from threading import Thread


@dp.message_handler(commands="send_all", is_admin=True)
async def _sender(message: Message, state):
    text = _("Введи текст")

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))

    await Sender.text_all.set()

    async with state.proxy() as data:
        data['message'] = list()
        data['message'].append(message.message_id)
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=Sender.text_all, content_types=ContentTypes.ANY, menu=False)
async def get_text(message: Message, state):
    if message.content_type != 'text':
        text = _('Ты прислал мне {type}, а нужно прислать текст').format(type=message.content_type)
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    t_s = Thread(target=between_callback, args=(sender, message.text))

    t_s.start()

    async with state.proxy() as data:
        data['message'].append(message.message_id)

        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()

