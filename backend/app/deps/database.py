from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """异步数据库会话生成器"""
    async with async_session() as session:
        yield session


session_dep = Annotated[AsyncSession, Depends(get_session)]
