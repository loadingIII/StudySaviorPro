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

    async def retrieve_docs(self, query: str) -> list[Document]:
        """异步调用向量检索器,获取相关文档"""
        return await self.retriever.ainvoke(query)

    def assemble_context(self, docs: list[Document]) -> str:
        """将检索到的文档组装为编号格式的上下文字符串"""
        content = ""
        for i, doc in enumerate(docs, 1):
            content += f"[参考资料{i}]:参考资料:{doc.page_content}|元数据:{doc.metadata}\n"
        return content

    async def retrieve_and_assemble(self, query: str) -> str:
        """异步检索并组装上下文"""
        docs = await self.retrieve_docs(query)
        return self.assemble_context(docs)


    async def rag_summarize(self, query: str) -> str:
        """RAG总结（向后兼容）"""
        content = await self.retrieve_and_assemble(query)
        return await self.chain.ainvoke(
            {"input": query, "context": content}
        )



if __name__ == '__main__':
    import asyncio
    rag_service = RagSummarizeService()
    print(asyncio.run(rag_service.rag_summarize("武汉有哪些好玩的?")))
