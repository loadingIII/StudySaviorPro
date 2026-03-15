from langchain_core.tools import tool
from agent.rag.rag_service import RagSummarizeService
from zai import ZhipuAiClient

from utils.envUtils import zhi_pu_api_key

rag = RagSummarizeService()


@tool(description="RAG工具,用于检索知识库相关信息并生成答案,传入用户问题,将用户问题与检索到的相关信息进行总结,生成提示词返回")
def rag_tool(query: str) -> str:
    """RAG工具,用于检索相关信息并生成答案

    Args:
         query: 用户查询

    Return:
        用户问题与检索到的相关信息生成的总结
    """
    return rag.rag_summarize(query)


@tool(description="Web搜索工具,用于从网络上搜索相关信息,并返回字符串信息")
def web_search(query: str) -> str:
    """Web搜索工具,用于从网络上搜索相关信息并生成答案

    Args:
         query: 用户查询

    Return:
        从网络上搜索相关信息生成的总结
    """
    client = ZhipuAiClient(api_key=zhi_pu_api_key)
    response = client.web_search.web_search(
        search_engine="search_std",
        search_query=query,
        count=5,  # 返回结果的条数，范围1-50，默认10
        search_domain_filter="www.baidu.com",  # 只访问指定域名的内容
        search_recency_filter="noLimit",  # 搜索指定日期范围内的内容
        content_size="high"  # 控制网页摘要的字数，默认medium
    )
    # print(response)
    return response


if __name__ == '__main__':
    # res = web_search("衡阳有哪些好玩的地方?")
    res = rag_tool("长沙有哪些好玩的?")
    # print(res)
