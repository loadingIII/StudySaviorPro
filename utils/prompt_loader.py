from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from utils.path_tool import get_abs_path


def get_prompt(prompt_name: str):
    file_path = get_abs_path(prompt_name)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

system_prompt = get_prompt("agent/prompts/system_prompt.txt")

rag_prompt = get_prompt("agent/prompts/rag_summarize.txt")
#智能出题提示词
choice_prompt = get_prompt("agent/prompts/smart_question/choice_question.txt")

fill_blank_prompt = get_prompt("agent/prompts/smart_question/fill_blank_question.txt")

tf_prompt = get_prompt("agent/prompts/smart_question/tf_question.txt")

cr_question_prompt = get_prompt("agent/prompts/smart_question/cr_question.txt")

#上下文压缩提示词
chat_zip_prompt = get_prompt("agent/prompts/chat_zip_prompt.txt")

#doc压缩提示词
docs_zip_prompt = get_prompt("agent/prompts/docs_zip_prompt.txt")



if __name__ == '__main__':
    print(docs_zip_prompt)