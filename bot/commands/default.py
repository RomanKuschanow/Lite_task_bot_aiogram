from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat, BotCommand
from models import User

from loader import _, bot


def get_default_commands(lang) -> list[BotCommand]:
    commands = [
        BotCommand('/start', _('запуск бота', locale=lang)),
        BotCommand('/help', _('список всех команд', locale=lang)),
        BotCommand('/new_reminder', _('новое напоминание', locale=lang)),
        BotCommand('/reminders_list', _('список всех напоминаний пользователя', locale=lang)),
        BotCommand('/donate', _('помочь развитию бота', locale=lang)),
        BotCommand('/feedback', _('оставить отзыв или пожелания', locale=lang)),
        BotCommand('/menu', _('Отобразить меню', locale=lang)),
        BotCommand('/remove_menu', _('Скрыть меню', locale=lang)),
        BotCommand('/lang', _('сменить язык', locale=lang)),
        BotCommand('/tz', _('выбрать часовой пояс', locale=lang)),
        BotCommand('/reset', _('сброс текущего действия', locale=lang))
    ]

    return commands


async def set_default_commands(is_admin: bool = False):
    commands_ru = get_default_commands('ru')
    commands_en = get_default_commands('en')

    await bot.set_my_commands(commands_ru, scope=BotCommandScopeDefault(), language_code='ru')
    await bot.set_my_commands(commands_en, scope=BotCommandScopeDefault(), language_code='en')


async def set_user_commands(id: int, lang: str, is_admin: bool = False):
    commands = get_default_commands(lang)

    await bot.set_my_commands(commands, scope=BotCommandScopeChat(id))
