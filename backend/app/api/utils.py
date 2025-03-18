import io
import os
import uuid

from loguru import logger
from PIL import Image
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.core import exceptions
from app.crud import get_user_by_email, get_user_by_username


async def check_existing_user(*, session: AsyncSession, username: str = None, email: EmailStr = None) -> None:
    """检查用户名和邮箱是否重复"""
    if username:
        existing_username = await get_user_by_username(session=session, username=username)
        if existing_username:
            raise exceptions.USER_NAME_ALREADY_EXISTS
    if email:
        existing_email = await get_user_by_email(session=session, email=email)
        if existing_email:
            raise exceptions.USER_EMAIL_ALREADY_EXISTS


def image_to_webp(
    *,
    image_data: io.BytesIO,
    output_path: str,
    is_thumbnail: bool = True,
    max_size: tuple = (200, 200),
    quality: int = 85,
) -> str:
    """将输入的图片数据转换为 WebP 格式并保存到指定目录"""
    try:
        with Image.open(image_data) as img:
            # 转换颜色模式以优化兼容性和质量
            if img.mode not in ("RGB", "RGBA"):
                if img.mode in ("LA", "PA", "P") and "A" in img.getbands():
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")

            # 缩略图，使用 LANCZOS 重采样算法
            if is_thumbnail:
                img.thumbnail(max_size, resample=Image.Resampling.LANCZOS)

            # 保存为 WebP，调整质量和编码方法
            output_buffer = io.BytesIO()
            img.save(output_buffer, format="WEBP", quality=quality, method=6)
            output_buffer.seek(0)

            with open(output_path, "wb") as f:
                f.write(output_buffer.getvalue())

            return output_path

    except Exception as e:
        logger.error(f"图片转换错误: {e}")
        raise exceptions.INVALID_FILE_FORMAT


def avatar_to_webp(*, image_data: io.BytesIO, id: int):
    output_dir = settings.AVATAR_DIR / str(id)
    filename = f"{id}_{uuid.uuid4().hex}.webp"
    tb_dir = output_dir / "tb"
    og_dir = output_dir / "og"
    os.makedirs(tb_dir, exist_ok=True)
    os.makedirs(og_dir, exist_ok=True)
    tb_path = tb_dir / filename
    og_path = og_dir / filename
    tb_path = image_to_webp(image_data=image_data, output_path=tb_path, is_thumbnail=True)
    og_path = image_to_webp(image_data=image_data, output_path=og_path, is_thumbnail=False)

    return filename
