from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings

from utils.configUtils import chroma_config
from utils.envUtils import qwen_api_key, qwen_url, qwen_model_name

chat_llm = ChatTongyi(
    model=qwen_model_name,
    temperature=0.7,
    api_key=qwen_api_key,
    base_url=qwen_url)

think_llm = ChatTongyi(
    model=qwen_model_name,
    temperature=0.5,
    api_key=qwen_api_key,
    base_url=qwen_url)


embd_model = DashScopeEmbeddings(model=chroma_config["embedding_model"])


if __name__ == "__main__":
    response = chat_llm.invoke("你是谁呀?")
    print(response)