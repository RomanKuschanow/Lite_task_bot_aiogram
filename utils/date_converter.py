from datetime import datetime


def date_convert(date) -> datetime:
    return datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)

