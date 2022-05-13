from datetime import datetime

from peewee import BigIntegerField, IntegerField, FloatField, CharField, BooleanField, DateTimeField, ForeignKeyField

from .base import BaseModel, database


class Bill(BaseModel):

    id = IntegerField(primary_key=True)

    label = CharField()
    status = CharField(null=True)
    amount = FloatField()

    user_id = BigIntegerField()

    created_at = DateTimeField(default=lambda: datetime.now())
    updated_at = DateTimeField(default=datetime.now)

    def __str__(self) -> str:
        return f'<Bill {self.id} amount={self.amount} label={self.label}>'

    class Meta:
        table_name = 'bills'
