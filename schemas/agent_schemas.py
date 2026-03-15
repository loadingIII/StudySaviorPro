from pydantic import BaseModel, Field


class AgentQuestion(BaseModel):
    question: str = Field(..., description="用户提出的问题")
    session_id: int = Field(default=1, description="用户会话ID，用于关联上下文")
