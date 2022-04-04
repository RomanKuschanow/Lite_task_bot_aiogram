from aiogram.types import Message, CallbackQuery, ContentTypes
from bot.keyboards.inline import get_inline_states_markup

from loader import dp, _, bot
from bot.states.admins import AddAdmin
from services.user import update_is_admin, get_user

from bot.states.admins.sender import Sender


@dp.message_handler(commands="send_private", is_admin=True)
async def _sender(message: Message, state, call_from_back=False):
    text = _("Введи id пользователя")

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))

    await Sender.id.set()

    async with state.proxy() as data:
        if not call_from_back:
            data['message'] = list()
            data['fail'] = 0
            data['message'].append(message.message_id)
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=Sender.id, content_types=ContentTypes.ANY, menu=False)
async def get_id(message: Message, session, state):
    if message.content_type != 'text':
        text = _('Ты прислал мне {type}, а нужно прислать текст').format(type=message.content_type)
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['fail'] += 1
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return
    if not message.text.isnumeric():
        text = _("Мне нужен набор цифр")
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup(True))
        async with state.proxy() as data:
            data['fail'] += 1
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    text = _("Введи текст")

    bot_message = await message.answer(text, reply_markup=get_inline_states_markup())

    await Sender.text_private.set()

    async with state.proxy() as data:
        for i in range(2 * data['fail']):
            await bot.delete_message(message.chat.id, data['message'][-2])
            data['message'].pop(-2)

        data['fail'] = 0
        data['id'] = int(message.text)
        data['message'].append(message.message_id)
        data['message'].append(bot_message.message_id)


@dp.message_handler(state=Sender.text_private, content_types=ContentTypes.ANY, menu=False)
async def get_text(message: Message, state):
    if message.content_type != 'text':
        text = _('Ты прислал мне {type}, а нужно прислать текст').format(type=message.content_type)
        bot_message = await message.answer(text, reply_markup=get_inline_states_markup())
        async with state.proxy() as data:
            data['fail'] += 1
            data['message'].append(message.message_id)
            data['message'].append(bot_message.message_id)
        return

    async with state.proxy() as data:
        await bot.send_message(data['id'], message.text)
        data['message'].append(message.message_id)

        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()


@dp.callback_query_handler(text='back', state=Sender.text_private)
async def back(callback_query: CallbackQuery, state, session, user):
    await callback_query.answer()
    await Sender.id.set()
    async with state.proxy() as data:
        for i in range(2 * (data['fail'] + 1) + 1):
            await bot.delete_message(callback_query.message.chat.id, data['message'][-1])
            data['message'].pop()

        data['fail'] = 0

    await _sender(callback_query.message, state, True)