from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI

from utils.configUtils import chroma_config
from utils.envUtils import MODEL_API, MODEL_URL, model_name, qwen_api_key

thinking_disabled = {"thinking": {"type": "disabled"}}

chat_llm = ChatOpenAI(
    api_key=MODEL_API,
    base_url=MODEL_URL,
    model=model_name,
    temperature=0.7,
    extra_body=thinking_disabled,
)

think_llm = ChatOpenAI(
    api_key=MODEL_API,
    base_url=MODEL_URL,
    model=model_name,
    temperature=0.5,
    extra_body=thinking_disabled,
)


embd_model = DashScopeEmbeddings(model=chroma_config["embedding_model"], dashscope_api_key=qwen_api_key)


if __name__ == "__main__":
    response = chat_llm.invoke("你是谁呀?")
    print(response)
