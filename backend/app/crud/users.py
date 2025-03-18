from pydantic import EmailStr
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate


async def create_user(*, session: AsyncSession, user_create: UserCreate) -> User:
    """创建用户"""
    user_data = user_create.model_dump(exclude={"password"})
    user_data["hashed_password"] = get_password_hash(user_create.password)

    async with session.begin():
        new_user = User(**user_data)
        session.add(new_user)
        await session.flush()  # 推送更改到数据库（生成ID等）
        await session.refresh(new_user)  # 刷新获取数据库默认值

    return new_user


async def update_user(*, session: AsyncSession, id: int, user_update: UserUpdate) -> User | None:
    """更新用户"""
    async with session.begin():
        stmt = update(User).where(User.id == id).values(**user_update.model_dump(exclude_unset=True)).returning(User)
        result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user(*, session: AsyncSession, id: int) -> User | None:
    async with session.begin():
        user = await session.get(User, id)
    return user


async def get_user_by_email(*, session: AsyncSession, email: EmailStr) -> User | None:
    async with session.begin():
        result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_user_by_username(*, session: AsyncSession, username: str) -> User | None:
    async with session.begin():
        result = await session.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def get_user_by_username_or_email(*, session: AsyncSession, username_or_email: str) -> User | None:
    async with session.begin():
        result = await session.execute(
            select(User).where((User.username == username_or_email) | (User.email == username_or_email))
        )
    return result.scalars().first()


async def get_user_count(*, session: AsyncSession) -> int:
    async with session.begin():
        result = await session.execute(select(func.count(User.id)))
    return result.scalar()


async def get_user_list(*, session: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    async with session.begin():
        result = await session.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def authenticate_user(*, session: AsyncSession, username_or_email: str, password: str) -> User | None:
    user = await get_user_by_username_or_email(session=session, username_or_email=username_or_email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None
