from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings

from utils.configUtils import chroma_config
from utils.envUtils import MODEL_API, MODEL_URL, model_name

chat_llm = ChatTongyi(
    model=model_name,
    temperature=0.7,
    api_key=MODEL_API,
    base_url=MODEL_URL)

think_llm = ChatTongyi(
    model=model_name,
    temperature=0.5,
    api_key=MODEL_API,
    base_url=MODEL_URL)


embd_model = DashScopeEmbeddings(model=chroma_config["embedding_model"])


if __name__ == "__main__":
    response = chat_llm.invoke("你是谁呀?")
    print(response)