from aiogram import executor

from loader import dp, bot, config
from models.base import create_async_database
from utils.misc.logging import logger
from bot.commands import set_default_commands, set_admin_commands
from services.user import get_user_language


async def on_startup(dispatcher):
    logger.info('Bot startup')

    session = await create_async_database()

    bot['session'] = session

    for admin_id in config.ADMINS:
        await bot.send_message(admin_id, 'Бот успешно запущен')
        try:
            await set_admin_commands(admin_id, await get_user_language(session, admin_id))
        except:
            continue

    from scheduler import t
    t.start()

    await set_default_commands()


if __name__ == '__main__':
    from bot.middlewares import setup_middleware
    from bot import filters, handlers

    setup_middleware(dp)

    executor.start_polling(dp, on_startup=on_startup)
