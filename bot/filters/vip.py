import inspect

from loader import bot, _
from services.reminder import get_all_actual_by_user_id


def vip(limit=None):
    def wrapper(func):
        async def decorator(*args, **kwargs):
            if 'user' not in kwargs:
                user = args[3]
                session = args[2]
            else:
                user = kwargs['user']
                session = kwargs['session']

            if not user:
                return False

            if user.is_admin or user.is_vip:
                return await _attributes_check(func, args, kwargs)

            reminders = await get_all_actual_by_user_id(session, user.id)

            text = _(
                'К сожалению разработчикам тоже нужно что-то кушать, по этому некоторые функции доступны только после '
                'доната. Это можно сделать введя команду /donate, а так же воспользовавшись реферальной ссылкой /referral')

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

    return wrapper


async def _attributes_check(func, args, kwargs: dict):
    func_args_list = inspect.getfullargspec(func).args

    kwargs = {k: v for k, v in kwargs.items() if k in func_args_list}

    return await func(*args, **kwargs)
