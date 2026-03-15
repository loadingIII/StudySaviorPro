import json
from typing import Any
from utils.configUtils import db_config
import redis.asyncio as redis

REDIS_HOST = db_config['redis_host']
REDIS_PORT = db_config['redis_port']
REDIS_DB = db_config['redis_db']


# 创建 Redis 的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,  # Redis 服务器的主机地址
    port=REDIS_PORT,  # Redis 端口号
    db=REDIS_DB,  # Redis 数据库编号，0~15
    decode_responses=True  # 是否将字节数据解码为字符串
)


