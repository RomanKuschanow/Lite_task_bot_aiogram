from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, String
from sqlalchemy.orm import relationship

from .base import db


class User(db):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(255), default=None)
    first_name = Column(String(255))
    last_name = Column(String(255), default=None)
    language = Column(String, default='ru')

    status = Column(String(255), default='user')

    reminders = relationship("Reminder", back_populates="user", lazy='selectin')

    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f'<User [{self.id}] {self.first_name} {self.last_name}>'
