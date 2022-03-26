from aiogram.types import BotCommandScopeDefault, BotCommand


def get_default_commands() -> list[BotCommand]:
    commands = [
        BotCommand('/start', 'запуск бота'),
        BotCommand('/help', 'список всех команд'),
        BotCommand('/new_reminder', 'новое напоминание'),
        BotCommand('/reminders_list', 'список всех напоминаний пользователья'),
        BotCommand('/feedback', 'оставить отзыв или пожелания'),
        BotCommand('/lang', 'сменить язык'),
        BotCommand('/reset', 'сброс текущего действия')
    ]

    return commands


async def set_default_commands():
    commands = get_default_commands()

    from loader import bot
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
