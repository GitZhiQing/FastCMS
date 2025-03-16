import ujson
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app import settings

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False,
    pool_size=15,  # 连接池
    max_overflow=10,  # 允许的额外连接
    pool_recycle=1800,  # 30 分钟回收连接
    future=True,  # 启用 2.x 风格
    json_serializer=ujson.dumps,  # 更快的 ujson 序列化
)
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
