from peewee import BigIntegerField, IntegerField, FloatField, CharField, BooleanField, DateTimeField, ForeignKeyField

from .base import BaseModel, database


class BannedUser(BaseModel):

    id = BigIntegerField(primary_key=True)

    user_id = BigIntegerField()

    ban_count = IntegerField()

    banned_until = DateTimeField()

    is_banned = BooleanField(default=False)

    class Meta:
        table_name = 'banned_users'
