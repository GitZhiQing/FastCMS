from typing import Annotated

from fastapi import Depends

from app.core import exceptions
from app.core.security import verify_token
from app.crud import get_user
from app.deps import session_dep, token_dep
from app.models import User
from app.schemas import TokenData


async def get_current_user(*, session: session_dep, token: token_dep) -> User:
    token_data: TokenData = verify_token(token)
    if token_data is None:
        raise exceptions.INVALID_CREDENTIALS

    current_user = await get_user(session=session, id=token_data.id)
    if current_user is None:
        raise exceptions.INVALID_CREDENTIALS

    return current_user


current_user_dep = Annotated[User, Depends(get_current_user)]


async def get_current_active_user(current_user: current_user_dep):
    if current_user.power < 1:  # BANED 用户
        raise exceptions.PERMISSION_DENIED


current_active_user_dep = Annotated[User, Depends(get_current_active_user)]
