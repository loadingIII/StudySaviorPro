from langchain_core.tools import tool

from agent.rag.rag_service import RagSummarizeService

_rag_service = RagSummarizeService()


@tool(description="从知识库中检索与 query 相关的文档内容，返回组装后的参考资料。在生成题目之前应先调用此工具获取参考资料。")
async def rag_retrieve(query: str) -> str:
    """从知识库中检索与 query 相关的文档内容，返回组装后的参考资料。在生成题目之前应先调用此工具获取参考资料。"""
    return await _rag_service.retrieve_and_assemble(query)
