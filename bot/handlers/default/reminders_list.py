from aiogram.types import Message, CallbackQuery, ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from loader import dp, _

from models import User
from services.reminder import get_all_by_user_id, get_all_actual_by_user_id, get_all_old_by_user_id
from bot.keyboards.inline import get_reminders_inline_markup


@dp.message_handler(commands='reminders_list')
async def reminders_list(message: Message, session: AsyncSession, user: User):
    text = _("У вас еще нет ни одного напоминания")

    if await get_list(get_all_by_user_id, session, user.id) != "":
        text = await get_list(get_all_by_user_id, session, user.id)

    await message.reply(text, reply_markup=get_reminders_inline_markup("all"))

@dp.callback_query_handler(text="all")
async def actual_reminders_list_callback(callback_query: CallbackQuery, session: AsyncSession, user: User):
    text = _("У вас еще нет ни одного напоминания")

    if await get_list(get_all_by_user_id, session, user.id) != "":
        text = await get_list(get_all_by_user_id, session, user.id)

    await callback_query.message.edit_text(text, reply_markup=get_reminders_inline_markup("all"))


@dp.message_handler(commands='actual_reminders_list')
async def actual_reminders_list(message: Message, session: AsyncSession, user: User):
    text = _("У вас нет предстоящих напоминаний")

    if await get_list(get_all_actual_by_user_id, session, user.id) != "":
        text = await get_list(get_all_actual_by_user_id, session, user.id)

    await message.reply(text, reply_markup=get_reminders_inline_markup("actual"))

@dp.callback_query_handler(text="actual")
async def actual_reminders_list_callback(callback_query: CallbackQuery, session: AsyncSession, user: User):
    text = _("У вас нет предстоящих напоминаний")

    if await get_list(get_all_actual_by_user_id, session, user.id) != "":
        text = await get_list(get_all_actual_by_user_id, session, user.id)

    await callback_query.message.edit_text(text, reply_markup=get_reminders_inline_markup("actual"))


@dp.message_handler(commands='old_reminders_list')
async def old_reminders_list(message: Message, session: AsyncSession, user: User):
    text = _("У вас еще нет старых напоминаний")

    if await get_list(get_all_old_by_user_id, session, user.id) != "":
        text = await get_list(get_all_old_by_user_id, session, user.id)

    await message.reply(text, reply_markup=get_reminders_inline_markup("old"))

@dp.callback_query_handler(text="old")
async def old_reminders_list_callback(callback_query: CallbackQuery, session: AsyncSession, user: User):
    text = _("У вас еще нет старых напоминаний")

    if await get_list(get_all_old_by_user_id, session, user.id) != "":
        text = await get_list(get_all_old_by_user_id, session, user.id)

    await callback_query.message.edit_text(text, reply_markup=get_reminders_inline_markup("old"))


async def get_list(function, *parametrs) ->str:
    text = ""

    for reminder in await function(parametrs[0], parametrs[1]):
        text += f'{"✅" if reminder.is_reminded else "❌"} {reminder.text}: {reminder.date.strftime("%d.%m.%Y %H:%M")}\n'

    return text
