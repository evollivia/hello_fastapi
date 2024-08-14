from datetime import datetime

from app.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime


class Member(Base):
    __tablename__ = 'member'
    mno = Column(Integer, autoincrement=True, primary_key=True, index=True)
    userid = Column(String, index=True)
    passwd = Column(String)
    name = Column(String)
    email = Column(String)
    regdate = Column(DateTime, default=datetime.now)