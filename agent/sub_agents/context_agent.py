from langchain.agents import create_agent
from langchain_core.tools import tool

from agent.llms.llms import think_llm
from agent.tool.rag_tool import rag_retrieve
from agent.tool.web_search_tool import web_search
from utils.logger_handler import logger
from utils.prompt_loader import context_fuse_prompt

_agent = create_agent(
    think_llm,
    tools=[rag_retrieve, web_search],
    system_prompt=context_fuse_prompt,
)


@tool(description="根据用户问题 query，自动调用 RAG 检索和 Web 搜索工具获取相关信息，返回组装后的参考资料供题目生成子智能体使用")
async def context_agent(query: str) -> str:
    """根据用户问题 query，自动调用 RAG 检索和 Web 搜索工具获取相关信息，返回组装后的参考资料供题目生成子智能体使用"""
    try:
        result = await _agent.ainvoke({"messages": [{"role": "user", "content": query}]})
        messages = result["messages"]
        # 从后往前找第一条有内容的非空消息
        for msg in reversed(messages):
            content = getattr(msg, "content", "") or ""
            if content.strip():
                return content.strip()
        return "无可用信息"
    except Exception as e:
        logger.error(f"context_agent 执行异常: {e}")
        return "无可用信息"
