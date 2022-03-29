from aiogram.types import BotCommandScopeDefault, BotCommand
from loader import _


def get_default_commands() -> list[BotCommand]:
    commands = [
        BotCommand('/start', _('запуск бота')),
        BotCommand('/help', _('список всех команд')),
        BotCommand('/new_reminder', _('новое напоминание')),
        BotCommand('/reminders_list', _('список всех напоминаний пользователья')),
        BotCommand('/donate', _('помочь развитию бота')),
        BotCommand('/feedback', _('оставить отзыв или пожелания')),
        BotCommand('/lang', _('сменить язык')),
        BotCommand('/tz', _('выбрать часовой пояс')),
        BotCommand('/reset', _('сброс текущего действия'))
    ]

    return commands


async def set_default_commands():
    commands = get_default_commands()

    from loader import bot
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
