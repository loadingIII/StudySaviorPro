# 题目生成子智能体 — 智能出题
# 内部 ReAct Agent 编排，Agent 自主决定调用 RAG / WebSearch / 题目生成工具
import re

from langchain.agents import create_agent
from langchain_core.tools import tool

from agent.llms.llms import think_llm
from agent.tool.rag_tool import rag_retrieve
from agent.tool.web_search_tool import web_search
from agent.tool.question_tools import (
    generate_choice_questions,
    generate_fill_blank_questions,
    generate_tf_questions,
    generate_cr_questions,
)
from utils.logger_handler import logger
from utils.prompt_loader import question_prompt

# 题目类型映射
QUESTION_TYPE_MAP = {
    0: "选择题",
    1: "填空题",
    2: "判断题",
    3: "主观题",
}

ALL_TOOLS = [rag_retrieve, web_search, generate_choice_questions, generate_fill_blank_questions, generate_tf_questions, generate_cr_questions]

agent = create_agent(
            think_llm,
            tools=ALL_TOOLS,
            system_prompt=question_prompt,
        )


def _clean_json_output(text: str) -> str:
    """去除 LLM 输出中的 markdown 代码块包裹，返回纯 JSON"""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    return cleaned.strip()


async def _run_core(query: str, question_type: int = 0, question_count: int = 1) -> str:
    """出题核心逻辑，供 @tool 和 API 入口共用"""
    type_name = QUESTION_TYPE_MAP.get(question_type, "选择题")
    enriched_query = (
        f"请生成题目：\n"
        f"【题目类型】{type_name}\n"
        f"【出题数量】{question_count}\n"
        f"【用户问题】{query}"
    )

    result = await agent.ainvoke({"messages": [{"role": "user", "content": enriched_query}]})
    final_message = result["messages"][-1].content
    final_message = _clean_json_output(final_message)

    logger.info(f"QuestionAgent 出题完成：query={query}, 类型={type_name}, 数量={question_count}")
    return final_message


@tool(description="""根据用户需求生成题目。直接传入参数：
- query: 用户问题（str，必填）
- question_type: 题目类型（int，0=选择题 1=填空题 2=判断题 3=主观题，默认0）
- question_count: 出题数量（int，默认1）""")
async def question_agent(query: str, question_type: int = 0, question_count: int = 1) -> str:
    """根据用户需求生成题目。@tool 包装，供 Supervisor 路由调用"""
    return await _run_core(query, question_type, question_count)


async def api_question_agent(query: str, question_type: int = 0, question_count: int = 1) -> str:
    """根据用户需求生成题目。无 @tool 包装，供 crud 层直接调用"""
    return await _run_core(query, question_type, question_count)


if __name__ == '__main__':
    import asyncio

    test_query = "请根据以下内容出题：教育的意义是什么？"
    # print(asyncio.run(question_agent(test_query, question_type=0, question_count=2)))
