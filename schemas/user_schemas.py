from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_serializer


class UserLogin(BaseModel):
    phone: str
    password: str


class UserResponse(BaseModel):
    """用户响应模型"""
    id: int
    Authorization: str