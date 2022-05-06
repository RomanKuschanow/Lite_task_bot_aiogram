from aiogram.types import Message

from bot.handlers.admin.add_admin import add_admin
from bot.handlers.admin.change_user_status import change_status
from bot.handlers.admin.send_all import _sender
from bot.handlers.admin.send_private import _sender as private_sender
from bot.handlers.admin.users_count import users_count
from bot.handlers.admin.export_table import export_table
from bot.handlers.default.menu import menu
from bot.keyboards.default.set_menu import set_menu
from services.settings import update_settings
from loader import dp, bot, _


@dp.message_handler(commands="admin_menu", is_admin=True)
async def admin_menu(message: Message, user, settings, session):
    settings.kb_enabled = True
    settings.last_kb = "admin"

    await update_settings(session, settings)

    await message.answer(_("Выбери действие из меню 👇"), reply_markup=set_menu(user))
    await message.delete()


@dp.message_handler(text="➕ Добавить Админа", state="*", is_admin=True)
@dp.message_handler(text="➕ Add Admin", state="*", is_admin=True)
@dp.message_handler(text="➕ Додати Адміна", state="*", is_admin=True)
async def new_admin(message: Message, state, session, user):
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
@dp.message_handler(text="🎁 Надати VIP", state="*", is_admin=True)
async def add_vip(message: Message, session, user, state):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await change_status(message, state)


@dp.message_handler(text="🔖 Рассылка", state="*", is_admin=True)
@dp.message_handler(text="🔖 Mailing", state="*", is_admin=True)
@dp.message_handler(text="🔖 Розсилка", state="*", is_admin=True)
async def mailing(message: Message, state):
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
@dp.message_handler(text="📫 Особисте повідомлення", state="*", is_admin=True)
async def personal(message: Message, session, user, state):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await private_sender(message, state)


@dp.message_handler(text="🔢 Количество пользователей", state="*", is_admin=True)
@dp.message_handler(text="🔢 Number of users", state="*", is_admin=True)
@dp.message_handler(text="🔢 Кількість користувачів", state="*", is_admin=True)
async def _users_count(message: Message, session, state):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await users_count(message, session)


@dp.message_handler(text="🗂 Таблицы", state="*", is_admin=True)
@dp.message_handler(text="🗂 Tables", state="*", is_admin=True)
@dp.message_handler(text="🗂 Таблиці", state="*", is_admin=True)
async def _users_count(message: Message, state):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await export_table(message)


@dp.message_handler(text="🧾 Меню", state="*", is_admin=True)
@dp.message_handler(text="🧾 Menu", state="*", is_admin=True)
async def _menu(message: Message, state, user, settings, session):
    settings.kb_enabled = True
    settings.last_kb = "main"

    await update_settings(session, settings)

    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await menu(message, user, settings, session)
