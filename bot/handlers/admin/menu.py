from aiogram.types import Message

from bot.handlers.default.menu import menu
from bot.handlers.admin.send_private import _sender as private_sender
from bot.handlers.admin.send_all import _sender
from bot.handlers.admin.change_user_status import change_status
from bot.handlers.admin.add_admin import add_admin
from bot.keyboards.default import get_menu_keyboard_markup, get_admin_keyboard_markup
from loader import dp, bot, _


@dp.message_handler(commands="admin_menu")
async def admin_menu(message: Message, user):
    await message.answer(_("Выбери действие из меню 👇"), reply_markup=get_admin_keyboard_markup())


@dp.message_handler(text="➕ Добавить Админа", state="*")
@dp.message_handler(text="➕ Add Admin", state="*")
async def _new_reminder(message: Message, state, session, user):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await add_admin(message, state)


@dp.message_handler(text="🎁 Выдать VIP", state="*")
@dp.message_handler(text="🎁 Issue VIP", state="*")
async def _reminders_list(message: Message, session, user, state):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await change_status(message, session)


@dp.message_handler(text="🔖 Рассылка", state="*")
@dp.message_handler(text="🔖 Newsletter", state="*")
async def _reminders_list(message: Message, state):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await _sender(message, state)


@dp.message_handler(text="📫 Личка", state="*")
@dp.message_handler(text="📫 Personal", state="*")
async def sender(message: Message, session, user, state):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await private_sender(message, state)


@dp.message_handler(text="🧾 Меню", state="*")
@dp.message_handler(text="🧾 Menu", state="*")
async def _menu(message: Message, state, user):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await menu(message, user)
