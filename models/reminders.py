from pendulum import now
from sqlalchemy import Column, Integer, BigInteger, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import db
import pytz


class Reminder(db):
    __tablename__ = 'reminder'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    user = relationship('User', back_populates='reminders')

    text = Column(String)

    date = Column(DateTime, default=now().add(minutes=30))

    is_reminded = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self) -> str:
        server_date = pytz.timezone('UTC').localize(self.date)

        date = server_date.astimezone(pytz.timezone(self.user.time_zone))
        return f'{self.text}: {date.strftime("%d.%m.%Y %H:%M")}'
