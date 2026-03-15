import asyncio
import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from agent.agent import agent_invoke, agent_stream
from crud.ai_response_service import crud_intelligent_question_generation, crud_get_user_generated_questions
from schemas.agent_schemas import AgentQuestion
from schemas.quesion_schemas import QuestionDTO
from schemas.result import success_response
from utils.dbUtils import get_db
from utils.logger_handler import logger

agent_router = APIRouter(
    prefix="/agent",
    tags=["agent"],)

@agent_router.post("/question/invoke")
async def ask_agent(data: AgentQuestion):
    # 在后台线程中运行同步的 agent_invoke，避免阻塞事件循环
    logger.info(f"用户调用Agent：{data.question}")
    res = await agent_invoke(data)
    data = {"response": res}
    return success_response(data=data, message="Agent response generated successfully")


@agent_router.post("/question/stream")
async def ask_agent_stream(data: AgentQuestion):
    logger.info(f"用户调用 Agent Stream：{data.question}")
    async def generate():
        full_response = ""
        async for chunk in agent_stream(data):
            if chunk:
                full_response += chunk
        
        if full_response:
            for char in full_response:
                payload = {"response": char}
                yield "data: " + json.dumps(success_response(data=payload, message="stream").dict(), ensure_ascii=False) + "\n\n"
                await asyncio.sleep(0.005)
        
        yield "event: done\n" + "data: " + json.dumps(success_response(data={"done": True}, message="finished").dict(), ensure_ascii=False) + "\n\n"

    headers = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no"
    }
    return StreamingResponse(generate(), media_type="text/event-stream", headers=headers)

@agent_router.post("/question/generate_question")
async def intelligent_question_generation(data:QuestionDTO,db:AsyncSession = Depends(get_db)):

    logger.info(f"用户请求智能出题：题目类型:{data.question_type} 出题数量:{data.question_count} 知识点:{data.question}")
    res = await crud_intelligent_question_generation(data, db)

    return success_response(data=res, message="智能出题成功")


@agent_router.get("/question/get_user_generated_questions")
async def get_user_generated_questions(db: AsyncSession = Depends(get_db)):
    """获取当前用户生成的所有题目记录"""
    res = await crud_get_user_generated_questions(db)
    return success_response(data=res, message="获取用户生成题目记录成功")
