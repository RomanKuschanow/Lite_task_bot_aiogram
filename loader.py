from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from data import config
from middlewares.i18n import i18n

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

if config.REDIS_HOST and config.REDIS_PORT:
    from aiogram.contrib.fsm_storage.redis import RedisStorage2
    storage = RedisStorage2(config.REDIS_HOST, config.REDIS_PORT, db=config.REDIS_DB)
else:
    from aiogram.contrib.fsm_storage.memory import MemoryStorage
    storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage, run_tasks_by_default=True)

_ = i18n.gettext

dp.middleware.setup(i18n)
