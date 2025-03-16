from fastapi import APIRouter

from app import crud
from app.deps.database import session_dep
from app.schemas.users import UserCreate, UserResp

router = APIRouter()


@router.post("/", response_model=UserResp)
async def create_user(session: session_dep, user_create: UserCreate) -> UserResp:
    """创建用户"""
    return await crud.create_user(session=session, user_create=user_create)
