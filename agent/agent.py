from langchain.agents import create_agent
from sqlalchemy.ext.asyncio import AsyncSession

from agent.llms.llms import chat_llm
from agent.llms.zip_llms import zip_chat_history
from crud.ai_response_service import crud_get_chat_history
from schemas.agent_schemas import AgentQuestion
from agent.memory.pg_memory import get_checkpointer, get_store
from agent.tool.base_tool import rag_tool,web_search
from utils.logger_handler import logger
from utils.prompt_loader import system_prompt
from langchain_core.messages import AIMessage
# 配置缓存
checkpointer = get_checkpointer()
store = get_store()

async def create_my_agent():

    # 创建agent
    return create_agent(
        chat_llm,
        tools=[web_search,rag_tool],
        system_prompt=system_prompt,
    )



async def agent_invoke(data: AgentQuestion):
    question = data.question
    """用于调用agent,并进行回答"""
    config = {"configurable": {"thread_id": "user_003"}}

    agent = await create_my_agent()
    res =await agent.ainvoke({"messages": [{"role": "user", "content": question}]}, config=config)
    # print(res)
    content = res["messages"][-1].content
    return content


async def agent_stream(db: AsyncSession,data: AgentQuestion):
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

    agent = await create_my_agent()
    input_dict = {
        "messages": [
            {"role": "user", "content": query},
        ]
    }
    response = agent.astream(input_dict, stream_mode="values", context={"report": False})
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
                pass    # 可能不是所有消息都有 tool_calls 属性，避免因缺失该属性而导致的错误
