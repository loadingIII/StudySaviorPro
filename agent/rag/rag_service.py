from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from agent.llms.llms import chat_llm
from agent.rag.vector_store import VectorStoreService
from utils.prompt_loader import rag_prompt
from langchain_core.prompts import PromptTemplate

class RagSummarizeService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.model = chat_llm
        self.prompt_text = PromptTemplate.from_template(rag_prompt)
        self.chain = self.__init__chain()


    def print_prompt(self, full_prompt):
        print("="*20,full_prompt.to_string(),"="*20)
        return full_prompt


    def __init__chain(self):
        """构建链条"""
        chain = self.prompt_text | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str) -> list[Document]:
        """调用向量检索器,获取相关文档"""
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        """RAG总结"""
        content_doc = self.retriever_docs(query)
        content = ""
        counter = 0
        for doc in content_doc:
            counter += 1
            content += f"[参考资料{counter}]:参考资料:{doc.page_content}|元数据:{doc.metadata}\n"

        return self.chain.invoke(
            {"input": query, "context": content}
        )



if __name__ == '__main__':
    rag_service = RagSummarizeService()
    print(rag_service.rag_summarize("武汉有哪些好玩的?"))
