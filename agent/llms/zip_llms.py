import tiktoken
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from schemas.agent_schemas import ChatHistoryVO
from utils.envUtils import qwen_api_key, qwen_url, qwen_model_name
from utils.prompt_loader import zip_prompt

zip_llm_name = qwen_model_name

# 用于计算token
enc = tiktoken.get_encoding("cl100k_base")

zip_llm = ChatOpenAI(
    api_key=qwen_api_key,
    base_url=qwen_url,
    model=zip_llm_name,
    temperature=0.3,
)


async def zip_content(chat_history: str):
    """调用zip_llm将chat_history进行压缩"""
    prompt = PromptTemplate.from_template(zip_prompt)

    chain = prompt | zip_llm | StrOutputParser()

    res = chain.invoke({"chat_history": chat_history})
    return res

async def zip_chat_history(list_chat: list[ChatHistoryVO])-> str:
    """将list_chat拼接成字符串,判断是否需要压缩"""
    chat_history = ""
    for c in list_chat:
        if c.role == 0:
            chat_history += f"[[user: {c.content}]]\n"
        elif c.role == 1:
            chat_history += f"[[ai: {c.content}]]\n"
    num_tokens = len(enc.encode(chat_history))
    if num_tokens > 3000:
        res = await zip_content(chat_history)
    else:
        res = chat_history
    return res
