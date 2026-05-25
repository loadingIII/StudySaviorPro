from langchain_openai import ChatOpenAI
from utils.envUtils import MODEL_API, MODEL_URL, model_name
import tiktoken

chat_llm_name = model_name
think_llm_name = model_name
question_llm_name = model_name
query_llm_name = model_name

chat_llm = ChatOpenAI(
    api_key=MODEL_API,
    base_url=MODEL_URL,
    model=chat_llm_name,
    temperature=0.7,
)

think_llm = ChatOpenAI(
    api_key=MODEL_API,
    base_url=MODEL_URL,
    model=think_llm_name,
    temperature=0.5,
)


question_llm = ChatOpenAI(
    api_key=MODEL_API,
    base_url=MODEL_URL,
    model=think_llm_name,
    temperature=0.5,
)


query_llm = ChatOpenAI(
    api_key=MODEL_API,
    base_url=MODEL_URL,
    model=think_llm_name,
    temperature=0.5,
)




if __name__ == "__main__":
    response = chat_llm.invoke("你是谁呀?")
    print(response)