from pendulum import now
from datetime import datetime

from peewee import BigIntegerField, IntegerField, CharField, BooleanField, DateTimeField, ForeignKeyField

from .base import BaseModel, database

from .users import User

import pytz


class Reminder(BaseModel):

    id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='reminders')

    text = CharField()

    date = DateTimeField(default=lambda: now().add(minutes=30))

    is_repeat = BooleanField(default=False)
    repeat_count = IntegerField(default=-1, null=True)
    curr_repeat = IntegerField(default=1)
    repeat_until = DateTimeField(null=True)
    repeat_range = CharField(default='day')
    next_date = DateTimeField(default=lambda: now().add(minutes=30))

    is_reminded = BooleanField(default=False)
    is_deleted = BooleanField(default=False)

    def __str__(self) -> str:
        server_date = pytz.timezone("UTC").localize(self.next_date if self.is_repeat else self.date)

        date = server_date.astimezone(pytz.timezone(self.user.time_zone))
        return f'{"✅" if self.is_reminded else "❌"}{"🔁" if self.is_repeat else ""} {self.text}: {date.strftime("%d.%m.%Y %H:%M")}'

    class Meta:
        table_name = 'reminders'
