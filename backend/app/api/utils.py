from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exceptions
from app.crud import get_user_by_email, get_user_by_username


async def check_existing_user(*, session: AsyncSession, username: str = None, email: EmailStr = None) -> None:
    if username:
        existing_username = await get_user_by_username(session=session, username=username)
        if existing_username:
            raise exceptions.USER_NAME_ALREADY_EXISTS
    if email:
        existing_email = await get_user_by_email(session=session, email=email)
        if existing_email:
            raise exceptions.USER_EMAIL_ALREADY_EXISTS
