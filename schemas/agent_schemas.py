from pydantic import BaseModel, Field


class AgentQuestion(BaseModel):
    question: str = Field(..., description="用户提出的问题")
    session_id: int = Field(default=1, description="用户会话ID，用于关联上下文")


class ChatHistoryVO(BaseModel):
    id: int = Field(..., description="聊天记录 ID")
    session_id: int = Field(..., description="会话 ID")
    role: int = Field(..., description="角色：0=用户，1=AI")
    content: str = Field(..., description="消息内容")
    created_at: str = Field(..., description="创建时间")
    status: int = Field(default=0, description="状态：0=活跃，1=删除")

    class Config:
        from_attributes = True

class ChatSessionVO(BaseModel):
    id: int = Field(..., description="会话 ID")
    title: str = Field(..., description="会话标题")
    created_at: str = Field(..., description="创建时间")

    class Config:
        from_attributes = True