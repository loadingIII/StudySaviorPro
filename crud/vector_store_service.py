from datetime import datetime, timedelta

from fastapi import UploadFile, File
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from agent.rag.vector_store import VectorStoreService
from model.FileInfo import FileInfo
from schemas.file_schemas import FileVO
from utils.configUtils import chroma_config
from utils.file_handler import get_file_md5_hex
from utils.logger_handler import logger
from utils.redisUtils import redis_delete_by_prefix
from utils.threadUtils import get_user_id


async def crud_add_documents(db: AsyncSession,file: UploadFile = File(...)):
    file_md5_hex = get_file_md5_hex(file)
    res = await db.execute(select(FileInfo).where(FileInfo.hash_sha256 == file_md5_hex))
    if res.scalars().one_or_none():
        # 文件已经处理过了,直接返回
        return 1

    vs = VectorStoreService()
    flat = await vs.add_and_save_documents(file)
    if flat == 0:
        # 文件成功添加到向量数据库,将文件信息存储到数据库中
        # 1. 读取文件的全部内容
        await file.seek(0)  # 确保从文件的开头开始读取
        file_content = await file.read()
        # 2. 获取内容的长度，即为文件大小（以字节为单位）
        file_size = round(len(file_content)/ (1024*1024),3)  # 转换为MB

        file = FileInfo(
            uploaded_by_user_id=get_user_id(),
            original_name=file.filename,
            file_size=file_size,
            stored_path="xxxxxxxxx", #后期可以存储文件在服务器上的路径或者云存储的URL
            hash_sha256= file_md5_hex,
            created_at=datetime.now(),
            file_type=file.filename.split(".")[-1] if "." in file.filename else "unknown",
        )
        db.add(file)
        return 0
    else:
        return flat


async def crud_get_all_files(db: AsyncSession):
    """获取当前用户上传的所有文件的信息"""
    res = await db.execute(select(FileInfo))
    files = res.scalars().all()
    file_vos = [
        FileVO(
            id=file.id,
            original_name=file.original_name,
            file_size=file.file_size,
            file_type=file.file_type or "unknown",
            created_at=file.created_at.isoformat() if file.created_at else datetime.now().isoformat()
        )
        for file in files
    ]
    return file_vos

async def crud_delete_file(db: AsyncSession, file_id: int):
    """删除指定ID的文件"""
    user_id = get_user_id()
    vs = VectorStoreService()
    collection = vs.vector_store._client.get_collection(chroma_config["collection_name"])

    res = await db.execute(select(FileInfo).where(FileInfo.id == file_id))
    file = res.scalars().one_or_none()
    if not file:
        return False  # 文件不存在
    name = file.original_name
    try:
        await db.delete(file)
        #删除redis中与该文件相关的内容
        flag = redis_delete_by_prefix(f"{user_id}:{file.hash_sha256}")
        if flag > 0:
            logger.info(f"Redis中与文件 {file.original_name} 相关的内容已成功删除，共删除 {flag} 个键")
        else:
            raise Exception(f"未能删除Redis中与文件 {file.original_name} 相关的内容，可能没有找到对应的键")

        # 删除向量数据库中与该文件相关的向量数据,这里需要根据实际情况实现,例如可以根据文件名或者文件ID来删除对应的向量数据
        collection.delete(where={"source_filename_md5": file.hash_sha256})
        return name,True  # 删除成功
    except Exception as e:
        await db.rollback()  # 回滚数据库事务
        logger.error(f"删除文件失败: {e}")

        return name,False  # 删除失败



async def crud_get_file_sizes(db: AsyncSession):
    """获取当前用户上传的所有文件的大小总和"""
    res = await db.execute(select(func.sum(FileInfo.file_size)).where(FileInfo.uploaded_by_user_id == get_user_id()))
    file_sizes = res.scalars().one_or_none()
    return file_sizes

async def crud_get_file_counts(db: AsyncSession):
    """获取当前用户上传的所有文件的数量"""
    res = await db.execute(select(func.sum(FileInfo.id)).where(FileInfo.uploaded_by_user_id == get_user_id()))
    file_counts = res.scalars().one_or_none()
    return file_counts

async def crud_get_file_counts_at_week(db: AsyncSession):
    """获取用户本周上传的文件数量"""
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())  # 获取本周的开始日期
    res = await db.execute(
        select(func.count(FileInfo.id)).where(
            FileInfo.uploaded_by_user_id == get_user_id(),
            FileInfo.created_at >= start_of_week
        )
    )
    file_counts = res.scalars().one_or_none()
    return file_counts