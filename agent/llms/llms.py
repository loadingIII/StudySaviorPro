from langchain_openai import ChatOpenAI
from utils.envUtils import qwen_api_key, qwen_url, qwen_model_name

chat_llm = ChatOpenAI(
    api_key=qwen_api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model=qwen_model_name,  # 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    temperature=0.7,
)

think_llm = ChatOpenAI(
    api_key=qwen_api_key,
    base_url=qwen_url,
    model=qwen_model_name,
    temperature=0.5,
)

if __name__ == "__main__":
    response = chat_llm.invoke("你是谁呀?")
    print(response)