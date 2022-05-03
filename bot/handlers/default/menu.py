from aiogram.types import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from bot.handlers.default.donate import donate
from bot.handlers.default.help import help
from bot.handlers.default.reminders.new_reminder import new_reminder
from bot.handlers.default.reminders.reminders_list import reminders_list
from bot.handlers.default.referral import get_referral_link
from bot.keyboards.default.set_menu import set_menu
from services.settings import update_settings
from loader import dp, bot, _


@dp.message_handler(commands="menu")
async def menu(message: Message, user, settings, session):
    settings.kb_enabled = True
    settings.last_kb = "main"

    await update_settings(session, settings)

    await message.answer(_("Выбери действие из меню 👇"), reply_markup=set_menu(user))
    await message.delete()


@dp.message_handler(commands="remove_menu")
async def remove_menu(message: Message, user, settings, session):
    settings.kb_enabled = False

    await update_settings(session, settings)

    await message.answer(_("Клавиатура убрана. Вызвать ее можно командой /menu"), reply_markup=set_menu(user))
    await message.delete()


@dp.message_handler(text="➕ Новое напоминание", state="*")
@dp.message_handler(text="➕ New reminder", state="*")
@dp.message_handler(text="➕ Нове нагадування", state="*")
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
@dp.message_handler(text="📝 Список нагадувань", state="*")
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


@dp.message_handler(text="🛠 Админ-клавиатура", state="*")
@dp.message_handler(text="🛠 Admin keyboard", state="*")
@dp.message_handler(text="🛠 Адмін-клавіатура", state="*")
async def _reminders_list(message: Message, state, user, settings, session):
    settings.kb_enabled = True
    settings.last_kb = "admin"

    await update_settings(session, settings)

    await message.answer(_("Выбери действие из меню 👇"), reply_markup=set_menu(user))
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
@dp.message_handler(text="❔ Допомога по командам", state="*")
async def _help(message: Message, state, user):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await help(message, user)


@dp.message_handler(text="🔗 Реферальная ссылка", state="*")
@dp.message_handler(text="🔗 Referral link", state="*")
@dp.message_handler(text="🔗 Реферальне посилання", state="*")
async def referral(message: Message, state, session, user):
    async with state.proxy() as data:
        if 'message' in data:
            for mes in data['message']:
                try:
                    await bot.delete_message(message.chat.id, mes)
                except:
                    continue

    await state.finish()
    await get_referral_link(message, session, user)
