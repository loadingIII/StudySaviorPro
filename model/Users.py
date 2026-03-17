"""SQLAlchemy model for the `Users` table.

This mirrors the SQL:

create table Users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Use this model with the async session factory in `utils/dbUtils.py`.
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, func
from model.base import Base


class Users(Base):
    """ORM model for the Users table."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True,comment="用户ID")
    username = Column(String(255), nullable=False, unique=True,comment="用户名")
    phone = Column(String(255), nullable=False, unique=True,comment="手机号")
    password_hash = Column(String(255), nullable=False,comment="密码哈希")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"<Users(id={self.id!r}, username={self.username!r}, phone={self.phone!r})>"
