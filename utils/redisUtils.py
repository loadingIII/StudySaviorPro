import redis

from utils.logger_handler import logger
from utils.md5_tools import get_md5

# 连接 Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, password=123321)


doc_key_prefix = f"docs:redis"  # Redis 键的前缀


def redis_save_docs(docs: list, prefix: str):
    """将文本内容存入 redis"""
    try:
        for doc in docs:
            md5 = get_md5(doc.page_content)
            r.set(f"{prefix}:{md5}", doc.page_content)
    except Exception as e:
        logger.error(f"文档内容存入 Redis 失败：{e}")


def redis_get_docs(key: str) -> str:
    """从 Redis 中获取文档内容"""
    try:
        return r.get(key)
    except Exception as e:
        logger.error(f"从 Redis 中获取文档内容失败：{e}")


def redis_delete(key: str):
    """从 Redis 中删除文档内容"""
    try:
        r.delete(key)
    except Exception as e:
        logger.error(f"从 Redis 中删除文档内容失败：{e}")


def redis_delete_by_prefix(prefix: str):
    """批量删除指定前缀的所有 Redis 键"""
    try:
        cursor = 0
        deleted_count = 0

        key = f"{doc_key_prefix}:{prefix}:"
        key = key.replace(" ", "")
        while True:
            # SCAN 迭代器，每次返回一批键
            cursor, keys = r.scan(cursor=cursor, match=key+"*", count=100)
            if keys:
                # 批量删除
                r.delete(*keys)
                deleted_count += len(keys)
                print(f"已删除 {len(keys)} 个键，累计 {deleted_count} 个")
            # cursor 回到 0 表示遍历完成
            if cursor == 0:
                break
        logger.info(f"批量删除完成，共删除 {deleted_count} 个键")
        return deleted_count
    except Exception as e:
        logger.error(f"批量删除 Redis 前缀内容失败：{e}")
        return 0


if __name__ == "__main__":
    # docs = [
    #     Document(page_content="这是第一段内容"),
    #     Document(page_content="这是第二段内容"),
    #     Document(page_content="这是第三段内容"),
    # ]
    # redis_save_docs(docs,"test:")

    md5 = get_md5("这是第一段内容")
    print(redis_get_docs("test:" + md5))
