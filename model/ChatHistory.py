from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, DateTime, ForeignKey, Text, func

from model.base import Base


class ChatSession(Base):
    __tablename__ = 'chat_session'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now)


class ChatHistory(Base):
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('chat_session.id', ondelete='CASCADE'), nullable=False)
    role = Column(Integer, nullable=False)  # 0=user, 1=ai
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now)
    status = Column(Integer, default=0)  # 0=active, 1=deleted
