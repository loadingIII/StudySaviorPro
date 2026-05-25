import tiktoken
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from schemas.agent_schemas import ChatHistoryVO
from utils.envUtils import MODEL_API, MODEL_URL, model_name
from utils.prompt_loader import chat_zip_prompt, docs_zip_prompt

zip_llm_name = model_name

# 用于计算token
enc = tiktoken.get_encoding("cl100k_base")

zip_llm = ChatOpenAI(
    api_key=MODEL_API,
    base_url=MODEL_URL,
    model=zip_llm_name,
    temperature=0.3,
)


#TODO: 还未测试,需要测试zip_llm是否能够正确压缩文本,以及压缩后的文本是否能够被chat_llm正确理解
async def zip_text(docs: list[Document]) -> str:
    prompt = PromptTemplate.from_template(docs_zip_prompt)
    chain = prompt | zip_llm | StrOutputParser()
    text = ""
    for i,doc in enumerate(docs,1):
        text += f"文档{i}:{doc.page_content}\n\n"

    res = await chain.ainvoke({"docs": text})
    return res


async def zip_content(chat_history: str):
    """调用zip_llm将chat_history进行压缩"""
    prompt = PromptTemplate.from_template(chat_zip_prompt)

    chain = prompt | zip_llm | StrOutputParser()

    res = await chain.ainvoke({"chat_history": chat_history})
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

if __name__ == '__main__':
    import asyncio

    # 测试doc压缩
    doc1 = Document(page_content="BERT模型由Google AI团队于2018年10月发布，基于Transformer编码器架构，"
                                 "采用掩码语言模型与下句预测进行预训练。在GLUE基准测试中得分80.4，参数量约340M，"
                                 "核心作者包括Jacob Devlin与Ming-Wei Chang。", metadata={"source": "doc1"})
    doc2 = Document(page_content="Moderna公司于2023年5月公布mRNA癌症疫苗mRNA-4157的II期临床试验结果：与默克Keytruda联用，"
                                 "使高风险黑色素瘤患者复发或死亡风险降低44%。试验纳入157名患者，中位随访19.5个月，成果发表于"
                                 "《新英格兰医学杂志》", metadata={"source": "doc2"})
    docs = [doc1, doc2]
    async def test_zip():
        zip_res = await zip_text(docs)
        zip_res = eval(zip_res)
        print("压缩结果:",type(zip_res), zip_res)
    asyncio.run(test_zip())