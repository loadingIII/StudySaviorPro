from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from agent.llms.llms import think_llm
from langchain_core.prompts import PromptTemplate

from agent.rag.rag_service import RagSummarizeService
from schemas.quesion_schemas import QuestionDTO
from utils.prompt_loader import choice_prompt, fill_blank_prompt, tf_prompt, cr_question_prompt
from model.question_schemas import MultipleChoiceQuestions, MultipleFillBlankQuestions, MultipleTFQuestions, MultipleCRQuestions

rag_service = RagSummarizeService()


def get_questions(qus: QuestionDTO):
    qus_type = qus.question_type
    qus_question = qus.question
    qus_count = qus.question_count

    #用于返回结果的变量
    res = None

    def print_prompt(full_prompt):
        """打印最终生成的提示"""
        print("="*20,full_prompt.to_string(),"="*20)
        return full_prompt

    def get_choice_questions(qus_question:str, qus_count:int):
        """获取选择题"""
        prompt_template = PromptTemplate.from_template(choice_prompt)

        chain =prompt_template | print_prompt | think_llm.with_structured_output(MultipleChoiceQuestions)

        return chain.invoke({"question_count": qus_count, "input": qus_question,"context": rag_service.rag_summarize(qus_question)})

    def get_fill_blank_questions(qus_question:str, qus_count:int):
        """获取填空题"""
        prompt_template = PromptTemplate.from_template(fill_blank_prompt)

        chain = prompt_template | print_prompt | think_llm.with_structured_output(MultipleFillBlankQuestions)
        res = chain.invoke({"input": qus_question,"question_count": qus_count,"context": rag_service.rag_summarize(qus_question)})
        return res


    def get_tf_questions(qus_question:str, qus_count:int):
        """获取判断题"""
        prompt_template = PromptTemplate.from_template(tf_prompt)

        chain = prompt_template | think_llm.with_structured_output(MultipleTFQuestions)
        res = chain.invoke({"question_count": qus_count, "input": qus_question,"context": rag_service.rag_summarize(qus_question)})
        return res


    def get_cr_questions(qus_question:str, qus_count:int):
        """获取主观题"""
        prompt_template = PromptTemplate.from_template(cr_question_prompt)

        chain = prompt_template | think_llm.with_structured_output(MultipleCRQuestions)
        res = chain.invoke({"question_count": qus_count, "input": qus_question,"context": rag_service.rag_summarize(qus_question)})
        return res

    if qus_type == 0:
        res = get_choice_questions(qus_question, qus_count)
    elif qus_type == 1:
        res = get_fill_blank_questions(qus_question, qus_count)
    elif qus_type == 2:
        res = get_tf_questions(qus_question, qus_count)
    elif qus_type == 3:
        res = get_cr_questions(qus_question, qus_count)
    return res


if __name__ == '__main__':
    qus = QuestionDTO(question="明朝的历史", question_type=3, question_count=2)
    res = get_questions(qus)
    print(res)







