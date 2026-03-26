
from agent.rag.generate_queries import generate_queries
from agent.rag.vector_store import VectorStoreService

import numpy as np

from utils.threadUtils import set_user_id

# 初始化向量数据库类
vs = VectorStoreService()


def deduplicate_and_rank(all_results: list, doc_num: int = 3, k: int = 60) -> list:
    """实现对检索到的文档进行去重和重排序"""
    content_to_doc = {}  # {Document.page_content: Document, ...}
    doc_dict = {}  # {Document.page_content: score, ...}
    for doc in all_results:
        content = doc[0].page_content
        if content not in doc_dict:
            content_to_doc[content] = doc[0]

            score = 1 / (np.exp(-(doc[1] / 10000)) + 1)
            doc_dict[content] = score  # {Document.page_content: score, ...}
        else:
            # 如果内容已经存在，使用RRF公式对权值进行更新
            rank = doc_dict[content]
            doc_dict[content] += 1 / (rank + k)

    # 对结果进行排序, 返回排序后的结果
    ranked_results = sorted(
        doc_dict.items(),
        key=lambda x: x[1],
        reverse=True
    )
    return [(content_to_doc[content], score) for content, score in ranked_results][:doc_num]


def get_sorted_docs(query: str) -> list:
    """最终的调用,将查询语句多样化后,查询文档,获取排序后的文档"""
    # 生成多样化查询语句
    query_list = generate_queries(query)
    # 检索
    all_results = []
    for query in query_list:
        res = vs.search_with_scores(query)
        all_results.extend(res)
    # 去重排序
    final_res = deduplicate_and_rank(all_results)
    return final_res  # [(Document, score), ...]


if __name__ == "__main__":
    set_user_id(1)  # 设置用户ID，确保在测试时能够正确访问Redis中的数据

    query = "教育的作用是什么？"
    sorted_docs = get_sorted_docs(query)
    # 输出排序后的文档内容和相似度分数
    i = 1
    for doc, score in sorted_docs:
        print(f"文档{i}: {doc.page_content}\n||相似度分数: {score}\n\n")
        i += 1
    print("=" * 25)
    vs = VectorStoreService()
    list_docs = vs.get_full_content_from_redis([doc for doc, _ in sorted_docs])
    print("从Redis中获取的完整文档内容:")
    for i, content in enumerate(list_docs, 1):
        print(f"文档{i}: {content}\n\n")