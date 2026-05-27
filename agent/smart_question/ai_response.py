import json

from langchain_core.output_parsers import StrOutputParser

from agent.llms.llms import think_llm
from langchain_core.prompts import PromptTemplate

from schemas.quesion_schemas import QuestionDTO
from utils.prompt_loader import choice_prompt, fill_blank_prompt, tf_prompt, cr_question_prompt
from model.question_schemas import MultipleChoiceQuestions, MultipleFillBlankQuestions, MultipleTFQuestions, MultipleCRQuestions


def _parse_json(text: str):
    """从 LLM 输出中提取 JSON 并解析"""
    # 去除 markdown 代码块包裹
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    cleaned = cleaned.strip()
    return json.loads(cleaned)


async def get_choice_questions(qus_question: str, qus_count: int, context: str = ""):
    """获取选择题，context 由外部注入（RAG/WebSearch 结果）"""
    prompt_template = PromptTemplate.from_template(choice_prompt)
    chain = prompt_template | think_llm | StrOutputParser()
    raw = await chain.ainvoke({"question_count": qus_count, "input": qus_question, "context": context})
    return MultipleChoiceQuestions(**_parse_json(raw))


async def get_fill_blank_questions(qus_question: str, qus_count: int, context: str = ""):
    """获取填空题"""
    prompt_template = PromptTemplate.from_template(fill_blank_prompt)
    chain = prompt_template | think_llm | StrOutputParser()
    raw = await chain.ainvoke({"input": qus_question, "question_count": qus_count, "context": context})
    return MultipleFillBlankQuestions(**_parse_json(raw))


async def get_tf_questions(qus_question: str, qus_count: int, context: str = ""):
    """获取判断题"""
    prompt_template = PromptTemplate.from_template(tf_prompt)
    chain = prompt_template | think_llm | StrOutputParser()
    raw = await chain.ainvoke({"question_count": qus_count, "input": qus_question, "context": context})
    return MultipleTFQuestions(**_parse_json(raw))


async def get_cr_questions(qus_question: str, qus_count: int, context: str = ""):
    """获取主观题"""
    prompt_template = PromptTemplate.from_template(cr_question_prompt)
    chain = prompt_template | think_llm | StrOutputParser()
    raw = await chain.ainvoke({"question_count": qus_count, "input": qus_question, "context": context})
    return MultipleCRQuestions(**_parse_json(raw))


async def get_questions(qus: QuestionDTO, context: str = ""):
    """根据题目类型分发到对应的生成函数，context 由外部传入"""
    qus_type = qus.question_type
    qus_question = qus.question
    qus_count = qus.question_count

    if qus_type == 0:
        return await get_choice_questions(qus_question, qus_count, context)
    elif qus_type == 1:
        return await get_fill_blank_questions(qus_question, qus_count, context)
    elif qus_type == 2:
        return await get_tf_questions(qus_question, qus_count, context)
    elif qus_type == 3:
        return await get_cr_questions(qus_question, qus_count, context)
    return None


if __name__ == '__main__':
    qus = QuestionDTO(question="明朝的历史", question_type=3, question_count=2)
    res = get_questions(qus)
    print(res)







