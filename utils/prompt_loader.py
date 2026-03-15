from utils.path_tool import get_abs_path


def get_prompt(prompt_name: str):
    file_path = get_abs_path(prompt_name)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


rag_prompt = get_prompt("agent/prompts/rag_summarize.txt")

system_prompt = get_prompt("agent/prompts/system_prompt.txt")


#智能出题提示词
choice_prompt = get_prompt("agent/prompts/smart_question/choice_question.txt")

fill_blank_prompt = get_prompt("agent/prompts/smart_question/fill_blank_question.txt")

tf_prompt = get_prompt("agent/prompts/smart_question/tf_question.txt")

cr_question_prompt = get_prompt("agent/prompts/smart_question/cr_question.txt")






if __name__ == '__main__':
    print(tf_prompt)