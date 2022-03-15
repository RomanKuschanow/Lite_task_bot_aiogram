from sqlalchemy import Column, Integer, SmallInteger, BigInteger, DateTime, String, Boolean

from base import db


class Task(db):
    __tablename__ = 'task'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    user_id = Column(BigInteger)

    text = Column(String)

    end_date = Column(DateTime, default=None)

    priority = Column(SmallInteger, default=0)
    is_complete = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f'[] {self.task}, end date: {self.end_date}, complete: {self.is_complete}'

