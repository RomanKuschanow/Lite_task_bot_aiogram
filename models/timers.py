from .users import User

from peewee import BigIntegerField, IntegerField, CharField, BooleanField, DateTimeField, ForeignKeyField

from .base import BaseModel, database

from datetime import datetime


class Timer(BaseModel):
    id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='reminders')

    text = CharField()

    start_date = DateTimeField()
    end_date = DateTimeField()

    pause_date = DateTimeField(default=datetime(1, 1, 1, 0, 0))
    is_paused = BooleanField(default=False)

    is_work = BooleanField(default=True)

    def __str__(self) -> str:
        if not self.is_paused:
            s = f"{self.end_date - self.start_date}."
            sn = f"{self.end_date - datetime.now()}."
            return f'{self.text} {s[0:s.find(".")]} => {sn[0:sn.find(".")]}'
        else:
            s = f"{self.end_date - self.pause_date}."
            return f'▶ {self.text} {s[0:s.find(".")]}'

    class Meta:
        table_name = 'timers'
