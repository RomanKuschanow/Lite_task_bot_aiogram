from sqlalchemy import Column, Integer, SmallInteger, BigInteger, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import db


class Task(db):
    __tablename__ = 'task'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    user = relationship('User', back_populates='tasks')

    text = Column(String)

    end_date = Column(DateTime, default=None)

    priority = Column(SmallInteger, default=0)
    is_complete = Column(Boolean, default=False)

    is_deleted = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f'{self.task}' + f': {self.end_date}' if self.end_date else ''
