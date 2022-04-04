from aiogram.types import Message

from bot.handlers.admin.add_admin import add_admin
from bot.handlers.admin.change_user_status import change_status
from bot.handlers.admin.send_all import _sender
from bot.handlers.admin.send_private import _sender as private_sender
from bot.handlers.default.menu import menu
from bot.keyboards.default import get_admin_keyboard_markup
from loader import dp, bot, _


@dp.message_handler(commands="admin_menu", is_admin=True)
async def admin_menu(message: Message, user):
    await message.answer(_("Выбери действие из меню 👇"), reply_markup=get_admin_keyboard_markup())


@dp.message_handler(text="➕ Добавить Админа", state="*", is_admin=True)
@dp.message_handler(text="➕ Add Admin", state="*", is_admin=True)
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


@dp.message_handler(text="🎁 Выдать VIP", state="*", is_admin=True)
@dp.message_handler(text="🎁 Add VIP", state="*", is_admin=True)
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


@dp.message_handler(text="🔖 Рассылка", state="*", is_admin=True)
@dp.message_handler(text="🔖 Mailing", state="*", is_admin=True)
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


@dp.message_handler(text="📫 Личка", state="*", is_admin=True)
@dp.message_handler(text="📫 Personal", state="*", is_admin=True)
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


@dp.message_handler(text="🧾 Меню", state="*", is_admin=True)
@dp.message_handler(text="🧾 Menu", state="*", is_admin=True)
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
