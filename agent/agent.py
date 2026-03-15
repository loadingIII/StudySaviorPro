from langchain.agents import create_agent

from agent.llms.llms import chat_llm
from schemas.agent_schemas import AgentQuestion
from agent.memory.pg_memory import get_checkpointer, get_store
from agent.tool.base_tool import rag_tool,web_search
from utils.prompt_loader import system_prompt

# 配置缓存
checkpointer = get_checkpointer()
store = get_store()

async def create_my_agent():

    # 创建agent
    return create_agent(
        chat_llm,
        tools=[web_search,rag_tool],
        system_prompt=system_prompt,
        # checkpointer=checkpointer,
        # store=store,
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


async def agent_stream(data: AgentQuestion):
    query = data.question
    agent = await create_my_agent()
    input_dict = {
        "messages": [
            {"role": "user", "content": query},
        ]
    }
    last_content = ""
    async for chunk in agent.astream(input_dict, stream_mode="values", context={"report": False}):
        latest_message = chunk['messages'][-1]
        from langchain_core.messages import AIMessage
        if isinstance(latest_message, AIMessage):
            current_content = latest_message.content or ""
            if len(current_content) > len(last_content):
                delta = current_content[len(last_content):]
                last_content = current_content
                if delta.strip():
                    yield delta

