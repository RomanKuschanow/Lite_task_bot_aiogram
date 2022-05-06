from aiogram.types import BotCommandScopeChat, BotCommand

from loader import _, bot

from .default import get_default_commands


def get_admin_commands(lang) -> list[BotCommand]:
    commands = get_default_commands(lang)

    commands.extend([
        BotCommand('/add_admin', _('сделать пользователя администратором', locale=lang)),
        BotCommand('/change_user_status', _('выдать пользователю VIP-статус', locale=lang)),
        BotCommand('/send_all', _('отправить сообщение всем пользователям', locale=lang)),
        BotCommand('/send_private', _('отправить личное сообщение пользователю', locale=lang)),
        BotCommand('/admin_menu', _('вызвать админ-меню', locale=lang)),
        BotCommand('/users_count', _('получить количество пользователей', locale=lang)),
        BotCommand('/export_table', _('экспорт таблиц из базы', locale=lang))
    ])

    return commands


async def set_admin_commands(id: int, lang: str):
    commands = get_admin_commands(lang)

    await bot.set_my_commands(commands, scope=BotCommandScopeChat(id))

