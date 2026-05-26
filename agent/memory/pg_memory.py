import atexit

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore
from psycopg_pool import AsyncConnectionPool

from utils.configUtils import pg_url

# 配置数据库连接
DB_URI = pg_url
# 创建异步连接池（不自动 open）
pool = AsyncConnectionPool(conninfo=DB_URI, min_size=1, max_size=10)

atexit.register(pool.close)

_pool_opened = False


async def _ensure_pool_open():
    global _pool_opened
    if not _pool_opened:
        await pool.open()
        _pool_opened = True


async def get_checkpointer():
    """创建并返回一个AsyncPostgresSaver对象，用于检查点保存"""
    await _ensure_pool_open()
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup()
    return checkpointer


async def get_store():
    """创建并返回一个AsyncPostgresStore对象，用于存储agent的状态和数据"""
    await _ensure_pool_open()
    store = AsyncPostgresStore(pool)
    return store
