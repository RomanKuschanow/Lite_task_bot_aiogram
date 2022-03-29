from services.reminder import get_all_actual_by_user_id
from services.user import get_user
from loader import bot, _

from models.base import create_async_database
import inspect

def vip(limit = None):
    def vip(func):
        async def decorator(*args, **kwargs):
            session = kwargs['session']
            user = kwargs['user']
            reminders = await get_all_actual_by_user_id(session, user.id)

            text = _("К сожалению разработчикам тоже нужно что-то кушать, по этому некоторые функции, такие как фильтры, "
                     "редактирование или сохдание боее пяти активных напоминаний за раз станут доступны только после "
                     "небольшого денежного взноса. Насколько оценить этого бота, решаете вы, полный доступ к боту "
                     "откроеться после любой суммы. Вконце концов, никто не мешает вам задонанить еще раз, если вы того "
                     "пожелаете 😉. Это можно сделать введя доманду /donate")

            if not user:
                return False

            if user.is_admin:
                return await _attributes_check(func, args, kwargs)

            if user.is_vip:
                return await _attributes_check(func, args, kwargs)
            else:
                if limit:
                    if len(reminders) < 5:
                        return await _attributes_check(func, args, kwargs)
                    else:
                        await bot.send_message(user.id, text=text)
                        return False
                else:
                    await bot.send_message(user.id, text=text)
                    return False

        return decorator
    return vip


async def _attributes_check(func, args, kwargs: dict):
    func_args_list = inspect.getfullargspec(func).args

    kwargs = {k: v for k, v in kwargs.items() if k in func_args_list}

    return await func(*args, **kwargs)

