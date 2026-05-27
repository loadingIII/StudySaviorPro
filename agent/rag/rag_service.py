import asyncio

from langchain_core.documents import Document

from agent.rag.GetSortedDocs import get_sorted_docs
from utils.threadUtils import set_user_id


class RagSummarizeService:

    def assemble_context(self, docs: list[Document]) -> str:
        """将检索到的文档组装为编号格式的上下文字符串"""
        content = ""
        for i, doc in enumerate(docs, 1):
            content += f"[参考资料{i}]:参考资料:{doc.page_content}|元数据:{doc.metadata}\n\n"
        return content

    async def retrieve_and_assemble(self, query: str) -> str:
        """查询多样化 → 多路检索 → RRF 重排序 → 组装上下文"""
        docs_with_scores = await asyncio.to_thread(get_sorted_docs, query)
        docs = [doc for doc, _ in docs_with_scores]
        return self.assemble_context(docs)


if __name__ == "__main__":
    set_user_id(1)  # 设置用户ID，确保在测试时能够正确访问Redis中的数据
    query = "教育的作用是什么？"
    rag_service = RagSummarizeService()
    context = asyncio.run(rag_service.retrieve_and_assemble(query))
    print(context)
