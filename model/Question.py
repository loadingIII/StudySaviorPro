from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from model.base import Base


class ChoiceQuestion(BaseModel):
    """
    表示由AI生成的选择题的Pydantic模型。
    """
    # 题干
    question: str
    # 选项，使用字典形式，键为选项字母，值为选项内容
    options: Dict[str, str]
    # 正确答案，例如 'A', 'B', 'C', 'D'
    answer: str
    # 对答案的解释
    explanation: str

class MultipleChoiceQuestions(BaseModel):
    questions: List[ChoiceQuestion] = Field(description="A list of multiple choice questions")


class FillBlankQuestion(BaseModel):
    """表示由AI生成的填空题的Pydantic模型。"""
    question: str
    answer: str
    explanation: str

class MultipleFillBlankQuestions(BaseModel):
    questions: List[FillBlankQuestion]

class TFQuestion(BaseModel):
    """表示由AI生成的判断题的Pydantic模型。"""
    question: str
    answer: int  # 0表示False, 1表示True
    explanation: str

class MultipleTFQuestions(BaseModel):
    questions: List[TFQuestion]

class CRQuestion(BaseModel):
    """表示由AI生成的主观题的Pydantic模型。"""
    question: str
    answer: str
    explanation: str

class MultipleCRQuestions(BaseModel):
    questions: List[CRQuestion]



from sqlalchemy import Integer, String, Text, DateTime, func, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import Optional
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

