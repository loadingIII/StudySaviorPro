from langchain_core.tools import tool
from zhipuai import ZhipuAI

from utils.envUtils import zhi_pu_api_key


@tool(description="传入用户query,搜索实时网络信息，当知识库中的参考资料不足时，使用此工具补充相关信息")
async def web_search(query: str) -> str:
    """搜索实时网络信息，当知识库中的参考资料不足时，使用此工具补充相关信息"""
    client = ZhipuAI(api_key=zhi_pu_api_key)
    response = client.web_search.web_search(
        search_engine="search_std",
        search_query=query,
        count=5,
        search_domain_filter="www.baidu.com",
        search_recency_filter="noLimit",
        content_size="medium"
    )
    return response
