# Agent 入口模块
# 对外暴露 agent_invoke（同步调用）和 agent_stream（流式调用）两个接口
# 内部使用 Supervisor Agent 进行任务路由，替代了旧版单一的 create_agent
from langchain_core.messages import AIMessage
from sqlalchemy.ext.asyncio import AsyncSession

from agent.sub_agents.supervisor import create_supervisor
from agent.llms.zip_llms import zip_chat_history
from crud.ai_response_service import crud_get_chat_history
from schemas.agent_schemas import AgentQuestion
from utils.logger_handler import logger
from utils.threadUtils import get_user_id

# 延迟初始化的 Supervisor 单例
_supervisor = None


async def _get_supervisor():
    global _supervisor
    if _supervisor is None:
        _supervisor = await create_supervisor()
    return _supervisor


async def agent_invoke(data: AgentQuestion):
    """非流式 Agent 调用，返回完整回复"""
    question = data.question
    user_id = get_user_id()
    config = {"configurable": {"thread_id": user_id}}

    supervisor = await _get_supervisor()
    res = await supervisor.ainvoke(
        {"messages": [{"role": "user", "content": question}]},
        config=config,
    )
    content = res["messages"][-1].content
    return content


async def agent_stream(db: AsyncSession, data: AgentQuestion):
    """流式 Agent 调用，逐块 yield 回复内容
    从 DB 获取历史对话 → 压缩 → 拼接当前问题 → Supervisor 流式执行 → yield 每个 token
    """
    temp_history = await crud_get_chat_history(db, data.session_id)
    zip_history = await zip_chat_history(temp_history)
    query = f"""
    【历史对话】：
    ######(在下一个"######"出来前都是会话历史)
    {zip_history}
    ######
    【用户现在提问】：
    {data.question}
    """

    user_id = get_user_id()
    config = {"configurable": {"thread_id": user_id}}
    input_dict = {
        "messages": [
            {"role": "user", "content": query},
        ]
    }
    supervisor = await _get_supervisor()
    response = supervisor.astream(input_dict, stream_mode="values", config=config)
    async for line in response:
        if line:
            latest_message = line["messages"][-1]
            if isinstance(latest_message, AIMessage):
                content = latest_message.content or ""
                if content:
                    yield content

            try:
                if latest_message.tool_calls:
                    logger.info(f"工具调用结果：{[tc['name'] for tc in latest_message.tool_calls]}")
            except AttributeError:
                pass
