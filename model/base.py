"""Shared declarative base for ORM models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Common base that all ORM models inherit from."""
    pass
