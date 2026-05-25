from typing import Dict, List

from pydantic import BaseModel, Field


class ChoiceQuestion(BaseModel):
    """表示由AI生成的选择题的Pydantic模型。"""
    question: str
    options: Dict[str, str]
    answer: str
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
