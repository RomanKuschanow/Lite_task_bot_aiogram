from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Float, Sequence

from .base import db


class Bill(db):
    __tablename__ = 'bills'

    id = Column(Integer, Sequence('bills_id'), primary_key=True)

    label = Column(String)
    status = Column(String)
    amount = Column(Float)

    user_id = Column(Integer)

    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f'<Bill {self.id} amount={self.amount} label={self.label}>'
