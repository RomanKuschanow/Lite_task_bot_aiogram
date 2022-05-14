from datetime import datetime

from peewee import BigIntegerField, IntegerField, CharField, BooleanField, DateTimeField, ForeignKeyField

from .base import BaseModel, database


class User(BaseModel):

    id = BigIntegerField(primary_key=True)
    username = CharField(default=None, null=True)
    first_name = CharField()
    last_name = CharField(default=None, null=True)
    language = CharField(default='ru')
    time_zone = CharField(default='Europe/Kiev')

    is_vip = BooleanField(default=False)
    is_biba = BooleanField(default=False)

    is_admin = BooleanField(default=False)

    settings = CharField(null=True)

    created_at = DateTimeField(default=lambda: datetime.now(tz=None))
    referal_id = BigIntegerField(null=True)

    banned_until = DateTimeField(null=True)
    ban_count = IntegerField(default=0)
    is_banned = BooleanField(default=False)

    def __str__(self) -> str:
        return f'User [{self.id}] {self.first_name} {self.last_name}'

    class Meta:
        table_name = 'users'
