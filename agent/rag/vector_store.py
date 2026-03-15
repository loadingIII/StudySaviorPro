from fastapi import UploadFile
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agent.llms.qwen_llm import embd_model
from utils.configUtils import chroma_config
from utils.file_handler import pdf_loader, txt_loader, doc_loader
from utils.logger_handler import logger
from utils.path_tool import get_abs_path


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

    #这里需要改写,用户调用时需要传入文件对象,然后经过md5值计算,如果没有处理过,则进行处理,否则跳过
    def load_document(self,file: UploadFile):
        """
        从数据文件中读取数据,将其转化为向量存入向量数据库,
        要计算文件的MD5值做去重
        :return:
        """
        def get_file_loader(file: UploadFile):
            """根据文件路径,返回对应的文件加载器"""
            if file.filename.endswith("pdf"):
                return pdf_loader(file)
            elif file.filename.endswith("txt"):
                return txt_loader(file)
            elif file.filename.endswith("doc") or file.filename.endswith("docx"):
                return doc_loader(file)
            return []

        try:
            documents: list[Document] = get_file_loader(file)
            if not documents:
                logger.warning(f"[加载知识库]文件{file.filename}内无有效文本内容,跳过")
                return 2
                # 2.将文件分片
            spliter_documents: list[Document] = self.spliter.split_documents(documents)

            if not spliter_documents:
                logger.warning(f"[加载知识库]文件{file.filename}分片后无有效文本内容,跳过")
                return 2
            # 给每个分片添加元数据,记录来源文件名,方便后续检索时展示
            for doc in spliter_documents:
                doc.metadata["source_filename"] = file.filename

                # 3.将分片内容存入向量数据库
            self.vector_store.add_documents(spliter_documents)

            logger.info(f"[加载知识库]文件{file.filename}处理完成")
            return 0
        except Exception as e:
            logger.error(f"[加载知识库]文件{file.filename}处理失败,{e}")
            return 3




if __name__ == '__main__':
    # 将数据存入向量数据库
    vs = VectorStoreService()
    vs.load_document()
    # # 检索数据
    # retriever = vs.get_retriever()
    # res = retriever.invoke("衡阳有什么好玩的?")
    # for r in res:
    #     print(r.page_content)
    #     print("-"*20)
    # persist_directory = get_abs_path(chroma_config["persist_directory"])
    # print(persist_directory)