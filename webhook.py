import logging

from aiogram.utils.executor import start_webhook

from loader import dp, bot, config
from services.user import get_user_language
from utils.misc.logging import logger
from bot.commands import set_default_commands, set_admin_commands

logging.basicConfig(level=logging.INFO)

# webhook settings
WEBHOOK_HOST = config.WEBHOOK_HOST
WEBHOOK_PATH = config.WEBHOOK_PATH
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = config.WEBHOOK_PORT


async def on_startup(dp):
    logger.info('Bot startup')
    logger.info(f'{WEBHOOK_URL=}')

    await bot.set_webhook(WEBHOOK_URL)

    for admin_id in config.ADMINS:
        await bot.send_message(admin_id, 'Бот успешно запущен')
        try:
            await set_admin_commands(admin_id, get_user_language(admin_id))
        except:
            continue

    from scheduler import t_r, t_t
    t_r.start()
    t_t.start()

    await set_default_commands()


async def on_shutdown(dp):
    logger.warning('Shutting down..')

    await bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    logger.warning('Bye!')



if __name__ == '__main__':
    from bot.middlewares import setup_middleware
    from bot import filters, handlers

    setup_middleware(dp)

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
