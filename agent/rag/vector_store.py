from fastapi import UploadFile
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agent.llms.llms import embd_model
from agent.llms.zip_llms import zip_text
from utils.configUtils import chroma_config
from utils.file_handler import pdf_loader, txt_loader, doc_loader, get_file_md5_hex
from utils.logger_handler import logger
from utils.md5_tools import get_md5
from utils.path_tool import get_abs_path
from utils.redisUtils import redis_save_docs, redis_get_docs, doc_key_prefix
import ast

from utils.threadUtils import get_user_id


class VectorStoreService:
    """"
    一个简单的向量存储类，用于存储和检索向量数据。需要实现添加向量和查询相似向量的功能。
    需要有chroma数据库用于向量存储,还需要一个Spliter用于文本分片,
    """

    def __init__(self):
        # 初始化Chroma数据库连接
        persist_directory = get_abs_path(chroma_config["persist_directory"])
        self.vector_store = Chroma(
            collection_name=chroma_config["collection_name"],
            persist_directory=persist_directory,
            embedding_function=embd_model
        )



        # 初始化文本分片器
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separators"],
            length_function=len
        )

    def get_retriever(self):
        """获取向量检索器"""
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_config["k"]})

    def search_with_scores(self, query: str, k: int = chroma_config["k"]):
        """返回文档和相似度分数"""
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return results

    async def add_and_save_documents(self, file: UploadFile):
        """添加文档"""
        file_md5_hex = get_file_md5_hex(file)
        user_id = get_user_id()
        def get_file_loader(file: UploadFile):
            """根据文件路径，返回对应的文件加载器"""
            if file.filename.endswith("pdf"):
                return pdf_loader(file)
            elif file.filename.endswith("txt"):
                return txt_loader(file)
            elif file.filename.endswith("doc") or file.filename.endswith("docx"):
                return doc_loader(file)
            return []

        # 加载文档
        try:
            docs: list[Document] = get_file_loader(file)
            if not docs:
                logger.warning(f"[加载知识库] 文件{file.filename}内无有效文本内容，跳过")
                return 2

            # 分块
            split_docs = self.spliter.split_documents(docs)
            if not split_docs:
                logger.warning(f"[加载知识库] 文件{file.filename}分片后无有效文本内容，跳过")
                return 2

            # 批量压缩处理
            batch_size = 10  # 每批处理 10 个文档
            zip_docs = []

            for i in range(0, len(split_docs), batch_size):
                batch = split_docs[i:i + batch_size]
                logger.info(
                    f"[压缩处理] 第{len(batch)}个文档 (批次 {i // batch_size + 1}/{(len(split_docs) - 1) // batch_size + 1})")

                # 批量压缩
                compressed_batch = await zip_text(batch)

                # 解析压缩结果 (假设返回的是列表格式)
                try:
                    # 尝试将字符串解析为列表
                    if isinstance(compressed_batch, str):
                        compressed_list = ast.literal_eval(compressed_batch)
                    else:
                        compressed_list = compressed_batch

                    # 创建压缩后的文档
                    for j, doc in enumerate(batch):
                        doc_md5 = get_md5(doc.page_content)
                        zip_str = compressed_list[j] if j < len(compressed_list) else "无有效内容"

                        print(f"压缩前...:", doc.page_content, "\n\n")
                        print(f"压缩后...", zip_str, "\n\n")

                        zip_doc = Document(
                            page_content=zip_str,
                            metadata={
                                "md5": doc_md5,
                                "source_filename_md5": file_md5_hex
                            })
                        zip_docs.append(zip_doc)
                        logger.info(f"文档{doc_md5}已压缩完成")

                except Exception as e:
                    logger.error(f"解析压缩结果失败: {e}")
                    continue

            # 批量添加到向量数据库
            if zip_docs:
                self.vector_store.add_documents(zip_docs)
                logger.info(f"[加载知识库] 批量添加{len(zip_docs)}个压缩后的文档到向量数据库")

            # 持久化存储，并将分块内容存入 redis
            redis_save_docs(split_docs, f"{doc_key_prefix}:{user_id}:{file_md5_hex}")

            return 0
        except Exception as e:
            logger.error(f"[加载知识库] 文件{file.filename}处理失败,{e}")
            return 3

    def get_full_content_from_redis(self, docs) -> list[str]:
        user_id = get_user_id()
        """从Redis中获取文档的完整内容"""
        full_content = []
        for doc in docs:
            doc_md5 = doc.metadata.get("md5", "")
            source_filename_md5 = doc.metadata.get("source_filename_md5", "")
            if not doc_md5 and not source_filename_md5:
                logger.error("文档缺少MD5元数据，无法从Redis获取内容")
                continue
            redis_key = f"{doc_key_prefix}:{user_id}:{source_filename_md5}:{doc_md5}"
            # redis_key = f"{doc_key_prefix}:1:{source_filename_md5}:{doc_md5}"
            print(f"尝试从Redis获取文档内容，使用键: {redis_key}")
            temp_content = redis_get_docs(redis_key)
            if not temp_content:
                logger.error(f"未能从Redis中找到MD5为{doc_md5}的文档内容")
                continue
            full_content.append(temp_content)

        return full_content




if __name__ == '__main__':
    # 将数据存入向量数据库
    vs = VectorStoreService()
    vs.add_and_save_documents(get_abs_path("agent/data/洗涤养护.txt"))
