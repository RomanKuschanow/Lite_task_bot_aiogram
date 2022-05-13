from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from bot.keyboards.inline import get_inline_tz_markup
from bot.keyboards.default.set_menu import set_menu
from services.user import update_time_zone
from bot.states import TimeZone
from loader import dp, _, bot


@dp.message_handler(commands='tz')
async def time_zone(message: Message, user, state: FSMContext):
    bot_message = await message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, bot_message.message_id)

    text = _('Выберите ваш регион')

    await TimeZone.region.set()

    bot_message = await message.answer(text, reply_markup=get_inline_tz_markup())

    await message.delete()

    async with state.proxy() as data:
        data['message'] = list()
        data['message'].append(bot_message.message_id)


@dp.callback_query_handler(state=TimeZone.region)
async def region(callback_query: CallbackQuery, state):
    await callback_query.answer()
    text = _('Теперь выберите часовой пояс')

    await TimeZone.city.set()

    async with state.proxy() as data:
        data['region'] = callback_query.data
        await callback_query.message.edit_text(text, reply_markup=get_inline_tz_markup(callback_query.data))


@dp.callback_query_handler(state=TimeZone.city, text='back')
async def back(callback_query: CallbackQuery, state):
    await callback_query.answer()

    async with state.proxy() as data:
        for mes in data['message']:
            try:
                await bot.delete_message(callback_query.message.chat.id, mes)
            except:
                continue

    await state.finish()

    text = _('Выберите ваш регион')

    await TimeZone.region.set()

    bot_message = await callback_query.message.answer(text, reply_markup=get_inline_tz_markup())

    async with state.proxy() as data:
        data['message'] = list()
        data['message'].append(bot_message.message_id)


@dp.callback_query_handler(state=TimeZone.city)
async def city(callback_query: CallbackQuery, user, state):
    await callback_query.answer()
    async with state.proxy() as data:
        text = _('Ваш часовой пояс установлен на {region}/{city}').format(region=data['region'],
                                                                          city=callback_query.data)

        update_time_zone(user.id, f'{data["region"]}/{callback_query.data}')

        for mes in data['message']:
            try:
                await bot.delete_message(callback_query.message.chat.id, mes)
            except:
                continue

    await state.finish()

    await callback_query.message.answer(text, reply_markup=set_menu(user))

