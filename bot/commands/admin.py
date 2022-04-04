from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat, BotCommand
from models import User

from loader import _, bot

from .default import get_default_commands


def get_admin_commands(lang) -> list[BotCommand]:
    commands = get_default_commands(lang)

    commands.extend([
        BotCommand('/add_admin', _('Сделать пользователя администратором', locale=lang)),
        BotCommand('/change_user_status', _('Выдать пользователю VIP-статус', locale=lang)),
        BotCommand('/send_all', _('Отправить сообщение всем пользователям', locale=lang)),
        BotCommand('/send_private', _('Отправить личное сообщение пользователю', locale=lang)),
        BotCommand('/admin_menu', _('Вызвать админ-меню'))
    ])

    return commands


async def set_admin_commands(id: int, lang: str):
    commands = get_admin_commands(lang)

    await bot.set_my_commands(commands, scope=BotCommandScopeChat(id))

