import os
import sys
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastCMS"
    HOST: str = "127.0.0.1"
    PORT: int = 8080
    API_STR: str = "/api"
    SECRET_KEY: str

    # 超级管理员账户信息
    SUPERADMIN_NAME: str = "superadmin"
    SUPERADMIN_PASSWORD: str = "seek2geek"
    SUPERADMIN_EMAIL: str = "superadmin@seek2.team"

    # 项目路径
    APP_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = APP_DIR.parent / "data"
    STATIC_DIR: Path = APP_DIR.parent / "static"
    POST_IMAGES_DIR: Path = STATIC_DIR / "posts"
    AVATAR_DIR: Path = STATIC_DIR / "avatars"

    # 图片限制
    MAX_IMAGE_SIZE: int = 1024 * 1024 * 3  # 3MB
    ALLOWED_IMAGE_MIMES: set[str] = {
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
    }

    # TOKEN 过期时间
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 15  # 15 mins
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 days

    # 前端 URL（用于 CORS 设置）
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


class DevelopmentSettings(Settings):
    APP_ENV: str = "development"
    DEBUG: bool = True
    WORKERS: int = 1

    # 数据库
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """根据操作系统动态生成数据库(SQLite)路径"""
        if sys.platform.startswith("win"):
            prefix = "sqlite+aiosqlite:///"
        else:
            prefix = "sqlite+aiosqlite:////"
        return f"{prefix}{self.DATA_DIR}/dev.db"


class ProductionSettings(Settings):
    APP_ENV: str = "production"
    DEBUG: bool = False
    WORKERS: int = 4

    # 数据库
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """根据操作系统动态生成数据库(SQLite)路径"""
        if sys.platform.startswith("win"):
            prefix = "sqlite+aiosqlite:///"
        else:
            prefix = "sqlite+aiosqlite:////"
        return f"{prefix}data.db"


@lru_cache
def get_settings() -> DevelopmentSettings | ProductionSettings:
    load_dotenv(".env")
    app_env = os.getenv("APP_ENV", "development")
    return DevelopmentSettings() if app_env == "development" else ProductionSettings()
