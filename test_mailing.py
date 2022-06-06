import time
from asyncio import sleep

from aiogram.types import Message, ContentTypes, CallbackQuery
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import get_mailing_markup, get_lifetime_markup, get_yes_or_no_markup, \
    get_cancel_mailing_markup, get_chapters_markup
from keyboards.inline import get_start_mailing_markup
from loader import bot, dp
from services.mailing import create_mailing
from services.users import count_users, get_users_ids
from states import States
from utils.db.base import create_async_database
from utils.misc.logging import logger


@dp.message_handler(state=States.mailing, text='Готово', is_admin=True)
async def _mailing_select_delete_time(message: Message, user, session, state):
    await message.answer('Через сколько часов удалить сообщения?', reply_markup=get_lifetime_markup())
    await States.mailing_select_delete_time.set()


@dp.message_handler(state=States.mailing_select_delete_time, is_admin=True)
async def _mailing_delete_time(message: Message, user, session, state):
    if message.text.isnumeric() and int(message.text) < 48:
        lifetime_hours = int(message.text)

        lifetime = round(int(time.time() + (lifetime_hours * 3600)))

        async with state.proxy() as data:
            data['mailing_lifetime'] = lifetime
            data['mailing_lifetime_hours'] = lifetime_hours
            await message.answer('Закрепить сообщения?', reply_markup=get_yes_or_no_markup())
            await States.mailing_select_pin_option.set()
    else:
        await _mailing_select_delete_time(message, user, session, state)


@dp.callback_query_handler(text='mailing_start', state=States.mailing_start)
async def _start_mailing(call: CallbackQuery, user, state):
    session = await create_async_database()

    async with state.proxy() as data:
        messages = data['mailing']
        mailing_lifetime = data['mailing_lifetime']
        pin_messages = data['pin_messages']
        data['mailing_started'] = True

    users = await get_users_ids(session)
    status_message = call.message

    messages_count = 0
    fail_count = 0

    for user_count, user_to_mail in enumerate(users):
        for message_id in messages:
            if not messages_count % 20:
                await status_message.edit_text(f'Рассылка {user_count}/{len(users)}\n\n'
                                               f'Успешных сообщений: {messages_count - fail_count}\n'
                                               f'Не получилось отправить: {fail_count}\n')
                async with state.proxy() as data:
                    if 'mailing_cancel' in data and data['mailing_cancel']:
                        await status_message.answer('Рассылка остановлена ❌',
                                                    reply_markup=await get_chapters_markup(user, session))
                        await state.finish()
                        await States.default.set()
                        return await session.close()
                await sleep(3)

            messages_count += 1
            try:
                mailing_message = await bot.copy_message(user_to_mail, call.message.chat.id, message_id)
                await create_mailing(session, user_to_mail, mailing_message.message_id, mailing_lifetime)

                if pin_messages:
                    await bot.pin_chat_message(user_to_mail, mailing_message.message_id)
            except Exception as e:
                logger.error(f'id: {user_to_mail} exception: {e}')
                fail_count += 1

            if not messages_count % 1000:
                await sleep(60)

    await state.finish()
    await status_message.answer('Рассылка проведена', reply_markup=await get_chapters_markup(user, session))
    await States.default.set()

    await session.close()


@dp.message_handler(state=States.mailing_select_pin_option, is_admin=True)
async def _mailing_select_pin_option(message: Message, session, state):
    pin_messages = message.text == 'Да'

    async with state.proxy() as data:
        messages = data['mailing']
        data['pin_messages'] = pin_messages
        mailing_lifetime_hours = data['mailing_lifetime_hours']

    for message_id in messages:
        await bot.copy_message(message.from_user.id, message.chat.id, message_id)

    await message.answer(f'Рассылка на {await count_users(session)} человек\n'
                         f'Удалить через {mailing_lifetime_hours} часов\n'
                         f'Закрепить: {"✅" if pin_messages else "❌"}', reply_markup=get_start_mailing_markup())

    await message.answer('Можно остановить рассылку', reply_markup=get_cancel_mailing_markup())
    await States.mailing_start.set()


@dp.message_handler(state=States.mailing_start, is_admin=True)
async def _mailing_cancel(message: Message, session, state, user):
    mailing_cancel = message.text == 'Остановить рассылку ❌'

    async with state.proxy() as data:
        if 'mailing_started' not in data:
            await message.answer('Рассылка отменена ❌',
                                 reply_markup=await get_chapters_markup(user, session))
            await state.finish()
            return await States.default.set()

        if 'mailing_cancel' in data:
            return await message.answer('Рассылка уже останавливается, подождите пару секунд',
                                        reply_markup=ReplyKeyboardRemove())

        data['mailing_cancel'] = mailing_cancel

    if not mailing_cancel:
        return await message.answer('Чтобы остановить рассылку нажмине "Остановить рассылку ❌"',
                                    reply_markup=get_cancel_mailing_markup())

    await message.answer('Рассылка останавливается...', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=States.mailing, is_admin=True, content_types=ContentTypes.ANY)
async def _get_mailing_messages(message: Message, state):
    async with state.proxy() as data:
        if 'mailing' not in data:
            data['mailing'] = list()

        data['mailing'].append(message.message_id)

    await message.answer('Ок', reply_markup=get_mailing_markup())