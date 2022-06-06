import inspect

from loader import bot, _
from services.reminder import get_all_actual_by_user_id as get_all_actual_reminders_by_user_id
from services.timer import get_all_actual_by_user_id as get_all_timer_by_user_id


def vip(limit=None, item_type="reminder"):
    def wrapper(func):
        async def decorator(*args, **kwargs):
            if 'user' not in kwargs:
                user = args[2]
            else:
                user = kwargs['user']

            if not user:
                return False

            if user.is_admin or user.is_vip:
                if item_type == "timer" and len(get_all_timer_by_user_id(user.id)) >= 25:
                    await bot.send_message(user.id, text=_("Нельзя создать больше 25 активных таймеров"))
                    return False
                return await _attributes_check(func, args, kwargs)

            if item_type == "reminder":
                items = get_all_actual_reminders_by_user_id(user.id)
            elif item_type == "timer":
                items = get_all_timer_by_user_id(user.id)

            text = _(
                'К сожалению разработчикам тоже нужно что-то кушать, по этому некоторые функции доступны только после '
                'доната. Это можно сделать введя команду /donate, а так же воспользовавшись реферальной ссылкой /referral')

            if limit:
                if len(items) < limit:
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
