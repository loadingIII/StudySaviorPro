from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from model.base import Base


class UserGeneratedQuestion(Base):
    """
    用户生成题目的记录模型 (ORM 映射)
    对应数据库表: user_generated_questions
    """
    __tablename__ = 'user_generated_questions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="记录的唯一ID")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    original_question: Mapped[str] = mapped_column(Text, nullable=False, comment="用户提交的原始问题")
    generated_question_text: Mapped[str] = mapped_column(Text, nullable=False, comment="AI生成的题目内容")
    question_type: Mapped[int] = mapped_column(Integer, nullable=False, comment="题目类型")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=datetime.now, comment="记录创建时间")

    def __repr__(self):
        return f"<UserGeneratedQuestion(id={self.id}, user_id={self.user_id}, question='{self.original_question[:20]}...')>"
