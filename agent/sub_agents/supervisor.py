# Supervisor 智能体 — 路由分发
# 将所有子智能体注册为 Tool，根据用户问题内容自动路由分发
# 历史对话已通过 DB 注入用户消息，不依赖 LangGraph checkpointer
from langchain.agents import create_agent

from agent.llms.llms import chat_llm
from agent.sub_agents.question_agent import question_agent
from agent.sub_agents.context_agent import context_agent
from utils.prompt_loader import system_prompt


def get_sub_agent_tools():
    """收集所有子智能体工具，供 create_supervisor 注册"""
    return [
        context_agent,
        question_agent,
    ]


async def create_supervisor(tools: list = None):
    """创建 Supervisor Agent
    将子智能体工具注册为 Agent 的可用工具。
    历史对话已通过 DB 注入用户消息，无需 checkpointer。
    """
    if tools is None:
        tools = get_sub_agent_tools()
    return create_agent(
        chat_llm,
        tools=tools,
        system_prompt=system_prompt,
    )
