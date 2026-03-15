from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
from psycopg_pool import ConnectionPool

from utils.configUtils import pg_url

# 配置数据库连接
DB_URI = pg_url
# 创建连接池
pool = ConnectionPool(conninfo=DB_URI, min_size=1, max_size=10, open=True)

def get_checkpointer():
    """创建并返回一个PostgresSaver对象，用于检查点保存"""
    checkpointer = PostgresSaver(pool)
    checkpointer.setup()
    return checkpointer

def get_store():
    """创建并返回一个PostgresStore对象，用于存储agent的状态和数据"""
    store = PostgresStore(pool)
    return store
