from aiogram.types import Message

from bot.handlers.default.donate import donate
from bot.handlers.default.help import help
from bot.handlers.default.reminders.new_reminder import new_reminder
from bot.handlers.default.reminders.reminders_list import reminders_list
from bot.keyboards.default.menu import get_menu_keyboard_markup
from loader import dp, bot, _


@dp.message_handler(commands="menu")
async def menu(message: Message):
    await message.answer(_("Выбери действие из меню 👇"), reply_markup=get_menu_keyboard_markup())


@dp.message_handler(text="➕ Новое напоминание", state="*")
@dp.message_handler(text="➕ New reminder", state="*")
async def _new_reminder(message: Message, state, session, user):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await new_reminder(message, state, session, user)


@dp.message_handler(text="📝 Список напоминаний", state="*")
@dp.message_handler(text="📝 Reminder List", state="*")
async def _reminders_list(message: Message, session, user, state):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await reminders_list(message, session, user)


@dp.message_handler(text="🛠 Админ клавиатура", state="*")
@dp.message_handler(text="🛠 Admin keyboard", state="*")
async def _reminders_list(message: Message, state):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()


@dp.message_handler(text="💵 Донат", state="*")
@dp.message_handler(text="💵 Donat", state="*")
async def _donate(message: Message, session, user, state):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await donate(message, state)


@dp.message_handler(text="❔ Помощь по командам", state="*")
@dp.message_handler(text="❔ Help by commands", state="*")
async def _help(message: Message, state):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await help(message)
