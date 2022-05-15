import pytz
from datetime import datetime


def get_text(reminder) -> str:
    from loader import _
    text = _("{reminder}\n"
             "Повторение: {repeat}\n").format(reminder=reminder, repeat=_("Да") if reminder.is_repeat else _("Нет"))

    if reminder.is_repeat:
        server_date = pytz.timezone("UTC").localize(reminder.date)

        date = server_date.astimezone(pytz.timezone(reminder.user.time_zone))

        text += _("Изначальная дата: {date}\n").format(date=date.strftime("%d.%m.%Y %H:%M"))

        if reminder.repeat_count:
            text += _("Количество повторений: {count}\n").format(
                count=reminder.repeat_count if reminder.repeat_count > 0 else _("Всегда"))

            if reminder.repeat_count > 0:
                text += _("Осталось: {left}\n").format(left=reminder.repeat_count - reminder.curr_repeat + 1)

        elif reminder.repeat_until:
            server_date = pytz.timezone("UTC").localize(reminder.repeat_until)

            date = server_date.astimezone(pytz.timezone(reminder.user.time_zone))

            date = datetime(date.year, date.month, date.day)

            text += _("Повторять до: {date}\n").format(date=date.strftime("%d.%m.%Y"))

        text += _("Частота повторений: {range}").format(range=reminder.repeat_range)

    return text
