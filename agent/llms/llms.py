from langchain_openai import ChatOpenAI
from utils.envUtils import MODEL_API, MODEL_URL, model_name
import tiktoken

chat_llm_name = model_name
think_llm_name = model_name
question_llm_name = model_name
query_llm_name = model_name

thinking_disabled = {"thinking": {"type": "disabled"}}

chat_llm = ChatOpenAI(
    api_key=MODEL_API,
    base_url=MODEL_URL,
    model=chat_llm_name,
    temperature=0.7,
    extra_body=thinking_disabled,
)

think_llm = ChatOpenAI(
    api_key=MODEL_API,
    base_url=MODEL_URL,
    model=think_llm_name,
    temperature=0.5,
    extra_body=thinking_disabled,
)


question_llm = ChatOpenAI(
    api_key=MODEL_API,
    base_url=MODEL_URL,
    model=think_llm_name,
    temperature=0.5,
    extra_body=thinking_disabled,
)


query_llm = ChatOpenAI(
    api_key=MODEL_API,
    base_url=MODEL_URL,
    model=think_llm_name,
    temperature=0.5,
    extra_body=thinking_disabled,
)




if __name__ == "__main__":
    response = chat_llm.invoke("你是谁呀?")
    print(response)
