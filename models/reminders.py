from pendulum import now
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import db
import pytz


class Reminder(db):
    __tablename__ = 'reminders'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    user = relationship('User', back_populates='reminders')

    text = Column(String)

    date = Column(DateTime, default=now().add(minutes=30))

    is_repeat = Column(Boolean, default=False)
    repeat_count = Column(Integer, default=-1)
    curr_repeat = Column(Integer, default=1)
    repeat_until = Column(DateTime, nullable=True)
    repeat_range = Column(String, default='day')

    is_reminded = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self) -> str:
        server_date = pytz.timezone("UTC").localize(self.date if self.is_repeat else self.date)

        date = server_date.astimezone(pytz.timezone(self.user.time_zone))
        return f'{"✅" if self.is_reminded else "❌"}{"🔁" if self.is_repeat else ""} {self.text}: {date.strftime("%d.%m.%Y %H:%M")}'
