import io
from typing import Annotated

from aiofiles import os as aiofiles_os
from fastapi import APIRouter, File, Path, Query, UploadFile
from loguru import logger
from pydantic import EmailStr

from app import crud, settings
from app.api.utils import avatar_to_webp, check_existing_user
from app.core import exceptions
from app.deps import current_user_dep, session_dep
from app.schemas import PaginatedResponse, UserCreate, UserResp, UserUpdate

router = APIRouter()


@router.get("", response_model=PaginatedResponse[UserResp])
async def read_user_list(
    session: session_dep,
    page: Annotated[int, Query(ge=1, description="页码", example=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100, description="每页数量", example=20)] = 20,
) -> PaginatedResponse[UserResp]:
    """获取用户列表"""
    skip = (page - 1) * per_page
    users = await crud.get_user_list(session=session, skip=skip, limit=per_page)
    total = await crud.get_user_count(session=session)

    return {
        "data": users,
        "meta": {"total": total, "page": page, "per_page": per_page, "total_pages": (total + per_page - 1) // per_page},
    }


@router.get("/{id}", response_model=UserResp)
async def read_user(session: session_dep, id: Annotated[int, Path(ge=1, description="用户 ID", example=1)]) -> UserResp:
    """通过用户 ID 获取用户信息"""
    user = await crud.get_user(session=session, id=id)
    if user is None:
        raise exceptions.USER_NOT_FOUND
    return user


@router.get("/email/{email}", response_model=UserResp)
async def read_user_by_email(
    session: session_dep, email: Annotated[EmailStr, Path(description="用户邮箱", example="seeker@example.com")]
) -> UserResp:
    """通过邮箱获取用户信息"""
    user = await crud.get_user_by_email(session=session, email=email)
    if user is None:
        raise exceptions.USER_NOT_FOUND
    return user


@router.get("/username/{username}", response_model=UserResp)
async def read_user_by_username(
    session: session_dep, username: Annotated[str, Path(description="用户名", example="Seeker")]
) -> UserResp:
    """通过邮箱获取用户信息"""
    user = await crud.get_user_by_username(session=session, username=username)
    if user is None:
        raise exceptions.USER_NOT_FOUND
    return user


@router.get("/me", response_model=UserResp)
async def read_current_user(current_user: current_user_dep) -> UserResp:
    """获取当前用户信息"""
    return current_user


@router.post("/", response_model=UserResp)
async def create_user(session: session_dep, user_create: UserCreate) -> UserResp:
    """创建用户"""
    await check_existing_user(session=session, username=user_create.username, email=user_create.email)
    user_created = await crud.create_user(session=session, user_create=user_create)
    return user_created


@router.patch("/{id}", response_model=UserResp)
async def update_user(
    session: session_dep,
    user_update: UserUpdate,
    current_user: current_user_dep,
    id: Annotated[int, Path(ge=1, description="用户 ID", example=1)],
) -> UserResp:
    """更新用户"""
    if user_update.username or user_update.email:
        await check_existing_user(session=session, username=user_update.username, email=user_update.email)
    if id != current_user.id:
        if current_user.id < 2:  # 非管理员
            raise exceptions.PERMISSION_DENIED
        user = await crud.get_user(session=session, id=id)
        if user is None:
            raise exceptions.RESOURCE_NOT_FOUND
        if current_user.power <= user.power:  # 越级操作
            raise exceptions.PERMISSION_DENIED

    user_updated = await crud.update_user(session=session, id=id, user_update=user_update)
    return user_updated


@router.patch("/{id}/avatar", response_model=UserResp)
async def update_user_avatar(
    session: session_dep,
    current_user: current_user_dep,
    id: Annotated[int, Path(ge=1, description="用户 ID", example=1)],
    avatar: UploadFile = File(...),
) -> UserResp:
    if id != current_user.id:
        raise exceptions.PERMISSION_DENIED
    user = await crud.get_user(session=session, id=id)
    if user is None:
        raise exceptions.USER_NOT_FOUND
    if avatar.content_type not in settings.ALLOWED_IMAGE_MIMES:
        raise exceptions.INVALID_FILE_FORMAT
    try:
        # 读取上传文件内容
        contents = await avatar.read()
        if len(contents) > settings.MAX_IMAGE_SIZE:
            raise exceptions.FILE_TOO_LARGE
        filename = avatar_to_webp(image_data=io.BytesIO(contents), id=id)
        if user.avatar is not None:
            old_tb_path = settings.AVATAR_DIR / str(id) / "tb" / filename
            old_og_path = settings.AVATAR_DIR / str(id) / "og" / filename
            for path in [old_tb_path, old_og_path]:
                try:
                    if await aiofiles_os.path.exists(path):
                        await aiofiles_os.remove(path)
                except Exception as e:
                    logger.error(f"删除用户 id={id} 删除头像错误: {e}")
        user = await crud.update_user(session=session, id=id, user_update=UserUpdate(avatar=filename))
        return user
    except Exception as e:
        logger.error(f"用户 id={id} 上传头像错误: {e}")
        raise exceptions.INTERNAL_SERVER_ERROR
