import asyncio
import json

from fastapi import APIRouter, Depends
from fastapi.params import Path, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from agent.agent import agent_invoke, agent_stream
from crud.ai_response_service import crud_intelligent_question_generation, crud_get_user_generated_questions, \
    crud_add_chat_history, crud_get_chat_history, crud_get_sessions, crud_get_new_session_id, crud_delete_chat_history, \
    crud_delete_chat_session
from schemas.agent_schemas import AgentQuestion
from schemas.quesion_schemas import QuestionDTO
from schemas.result import success_response, error_response
from utils.dbUtils import get_db
from utils.logger_handler import logger

agent_router = APIRouter(
    prefix="/agent",
    tags=["agent"], )


@agent_router.post("/question/invoke")
async def ask_agent(data: AgentQuestion):
    # 在后台线程中运行同步的 agent_invoke，避免阻塞事件循环
    logger.info(f"用户调用Agent：{data.question}")
    res = await agent_invoke(data)
    data = {"response": res}
    return success_response(data=data, message="Agent response generated successfully")


@agent_router.post("/question/stream")
async def ask_agent_stream(data: AgentQuestion, db: AsyncSession = Depends(get_db)):
    logger.info(f"用户调用 Agent Stream：{data.question}")

    async def generate():
        full_response = ""  # 用于存储完整的响应内容
        async for chunk in agent_stream(db,data):
            if chunk:
                full_response += chunk
                for char in chunk:
                    payload = {"response": char}
                    yield "data: " + json.dumps(success_response(data=payload, message="stream").model_dump(),
                                                ensure_ascii=False) + "\n\n"
                    await asyncio.sleep(0.01)  # 添加微小的延迟，模拟流式输出的效果
        # 将完整的响应内容存储到数据库中
        await crud_add_chat_history(db, data, full_response)
        yield "event: done\n" + "data: " + json.dumps(
            success_response(data={"done": True}, message="finished").model_dump(),
            ensure_ascii=False) + "\n\n"

    headers = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no"
    }
    return StreamingResponse(generate(), media_type="text/event-stream", headers=headers)


@agent_router.get("/question/get_new_session_id")
async def get_session_id(db: AsyncSession = Depends(get_db)):
    """获取当前用户的session_id"""
    session_id = await crud_get_new_session_id(db)
    return success_response(data=session_id, message="获取会话ID成功")


@agent_router.get("/question/get_chat_sessions")
async def get_chat_sessions(db: AsyncSession = Depends(get_db)):
    """获取当前用户的所有会话"""
    res = await crud_get_sessions(db)
    return success_response(data=res, message="获取用户会话成功")


@agent_router.get("/question/get_chat_history/{session_id}")
async def get_chat_history(session_id: int = Path(...), db: AsyncSession = Depends(get_db)):
    """获取当前用户的聊天记录"""
    res = await crud_get_chat_history(db, session_id)
    return success_response(data=res, message="获取用户聊天记录成功")

@agent_router.post("/question/delete_chat_history")
async def delete_chat_history(chat_history_ids: list[int] = Body(...), db: AsyncSession = Depends(get_db)):
    """删除当前用户的聊天记录"""
    flat = await crud_delete_chat_history(db, chat_history_ids)
    if not flat:
        return error_response(message="删除用户聊天记录失败")

    return success_response(message="删除用户聊天记录成功")

@agent_router.delete("/question/delete_chat_session/{session_id}")
async def delete_chat_session(session_id: int = Path(...), db: AsyncSession = Depends(get_db)):
    """删除当前用户的聊天会话"""
    flat = await crud_delete_chat_session(db, session_id)
    if not flat:
        return error_response(message="删除用户聊天会话失败")

    return success_response(message="删除用户聊天会话成功")




@agent_router.post("/question/generate_question")
async def intelligent_question_generation(data: QuestionDTO, db: AsyncSession = Depends(get_db)):
    logger.info(f"用户请求智能出题：题目类型:{data.question_type} 出题数量:{data.question_count} 知识点:{data.question}")
    res = await crud_intelligent_question_generation(data, db)
    return success_response(data=res, message="智能出题成功")


@agent_router.get("/question/get_user_generated_questions")
async def get_user_generated_questions(db: AsyncSession = Depends(get_db)):
    """获取当前用户生成的所有题目记录"""
    res = await crud_get_user_generated_questions(db)
    return success_response(data=res, message="获取用户生成题目记录成功")
