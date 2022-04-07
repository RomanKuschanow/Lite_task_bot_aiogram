from datetime import datetime

from sqlalchemy import Column, Integer, BigInteger, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import db


class Settings(db):
    __tablename__ = 'settings'

    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    user = relationship('User', back_populates='settings')

    kb_enabled = Column(Boolean, default=True)
    last_kb = Column(String, default="main")

    def __repr__(self) -> str:
        return f'Settings [{self.user_id}] {self.kb_enabled}, {self.last_kb}'
