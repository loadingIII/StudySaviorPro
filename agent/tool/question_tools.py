from langchain_core.tools import tool

from agent.smart_question.ai_response import (
    get_choice_questions,
    get_fill_blank_questions,
    get_tf_questions,
    get_cr_questions,
)


@tool
async def generate_choice_questions(query: str, question_count: int, context: str) -> str:
    """生成指定数量的选择题（A/B/C/D 四个选项）。query 为用户问题，question_count 为题目数量，context 为参考资料（来自 rag_retrieve 或 web_search 的结果）"""
    result = await get_choice_questions(query, question_count, context)
    return result.model_dump_json()


@tool
async def generate_fill_blank_questions(query: str, question_count: int, context: str) -> str:
    """生成指定数量的填空题。query 为用户问题，question_count 为题目数量，context 为参考资料（来自 rag_retrieve 或 web_search 的结果）"""
    result = await get_fill_blank_questions(query, question_count, context)
    return result.model_dump_json()


@tool
async def generate_tf_questions(query: str, question_count: int, context: str) -> str:
    """生成指定数量的判断题（对/错）。query 为用户问题，question_count 为题目数量，context 为参考资料（来自 rag_retrieve 或 web_search 的结果）"""
    result = await get_tf_questions(query, question_count, context)
    return result.model_dump_json()


@tool
async def generate_cr_questions(query: str, question_count: int, context: str) -> str:
    """生成指定数量的主观题（简答/论述）。query 为用户问题，question_count 为题目数量，context 为参考资料（来自 rag_retrieve 或 web_search 的结果）"""
    result = await get_cr_questions(query, question_count, context)
    return result.model_dump_json()
