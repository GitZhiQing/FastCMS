import time
from datetime import timedelta
from typing import Any

import bcrypt
from jose import JWTError, jwt

from app import settings
from app.schemas.tokens import TokenData

ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证哈希"""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    """生成哈希"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


async def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS),
) -> str:
    """生成访问令牌"""
    to_encode = data.copy()  # 需要编码进 JWT 的数据
    expire = int(time.time()) + expires_delta.total_seconds()  # 过期时间(UTC 时间戳)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_refresh_token(
    data: dict[str, Any],
    expires_delta: timedelta = timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS),
) -> str:
    """生成刷新令牌"""
    to_encode = data.copy()
    expire = int(time.time()) + expires_delta.total_seconds()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(token: str) -> TokenData | None:
    """验证令牌"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        uid: int = payload.get("sub")
        power: int = payload.get("power")
        if uid is None or power is None:
            return None
        return TokenData(uid=uid, power=power)
    except JWTError:
        return None
