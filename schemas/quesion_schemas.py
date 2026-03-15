from pydantic import BaseModel, Field


class QuestionDTO(BaseModel):
    question: str
    question_type: int
    question_count: int = Field(default=1, description="生成题目的数量，默认为1")



class UserGeneratedQuestionVO(BaseModel):
    id: int
    original_question: str
    generated_question_text: str
    question_type: int
    created_at: str