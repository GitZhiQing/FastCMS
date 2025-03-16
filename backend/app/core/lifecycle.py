import shutil
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from sqlalchemy import inspect

from app import settings
from app.core.database import async_engine, async_session


def folder_init():
    """文件夹初始化"""
    try:
        for path in [settings.DATA_DIR, settings.POST_IMAGES_DIR, settings.AVATAR_DIR]:
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"目录就绪: {path}")

    except FileNotFoundError as e:
        logger.critical(f"路径无效: {e.filename}")
        raise
    except PermissionError as e:
        logger.critical(f"权限不足: {e.filename}")
        raise


def folder_drop():
    """文件夹清理"""
    try:
        for path in [settings.POST_IMAGES_DIR, settings.AVATAR_DIR]:
            if path.exists():
                shutil.rmtree(path)
                logger.info(f"目录已清理: {path}")

    except OSError as e:
        logger.error(f"清理异常: {str(e)}")
        raise


async def db_init(force_drop: bool = False):
    """数据库初始化

    - force_drop: 是否强制删除重建（用于开发环境）
    """
    from app import models  # noqa
    from app.models.base import ModelBase

    try:
        async with async_engine.begin() as conn:
            if force_drop:
                await conn.run_sync(ModelBase.metadata.drop_all)
                logger.info("已强制删除旧表")

            await conn.run_sync(ModelBase.metadata.create_all)
            logger.info(f"数据库初始化{'并重建' if force_drop else '完成'}")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


async def db_drop():
    """删除数据库表"""
    from app import models  # noqa
    from app.models.base import ModelBase

    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(ModelBase.metadata.drop_all)
            logger.info("数据库清理完成")
    except Exception as e:
        logger.error(f"数据库清理失败: {e}")
        raise


async def create_super_admin():
    """创建超级管理员"""
    from app.core.security import get_password_hash
    from app.models.users import User

    try:
        async with async_session() as session:
            async with session.begin():
                superadmin = User(
                    username=settings.SUPERADMIN_NAME,
                    email=settings.SUPERADMIN_EMAIL,
                    hashed_password=get_password_hash(settings.SUPERADMIN_PASSWORD),
                    power=2,
                )
                session.add(superadmin)
                logger.info("超级管理员创建成功")
    except Exception as e:
        logger.error(f"超级管理员创建失败: {e}")
        raise


async def check_tables_exist() -> bool:
    """检查数据库表是否存在"""
    async with async_engine.begin() as conn:
        tables = await conn.run_sync(lambda db_conn: inspect(db_conn).get_table_names())
        return bool(tables)


async def create_test_user():
    """创建测试用户"""
    from app.core.security import get_password_hash
    from app.models.users import User

    try:
        async with async_session() as session:
            async with session.begin():
                test_super_admin = User(
                    username="test_super_admin",
                    email="test_super_admin@seek2.team",
                    hashed_password=get_password_hash("123456"),
                    power=3,
                )
                session.add(test_super_admin)
                test_admin = User(
                    username="test_admin",
                    email="admin@seek2.team",
                    hashed_password=get_password_hash("123456"),
                    power=2,
                )
                session.add(test_admin)

                test_users = []
                for i in range(4):
                    username = f"test_user_{i}"
                    test_user = User(
                        username=username,
                        email=f"{username}@seek2.team",
                        hashed_password=get_password_hash("123456"),
                    )
                    session.add(test_user)
                    test_users.append(test_user)
                logger.info("测试用户创建成功")
                return [test_super_admin, test_admin] + test_users
    except Exception as e:
        logger.error(f"测试用户创建失败: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info(
        f"应用 {app.title} 启动...\n"
        f"环境: {settings.APP_ENV}\n"
        f"调试: {settings.DEBUG}\n"
        f"主机: {settings.HOST}\n"
        f"端口: {settings.PORT}"
    )
    folder_init()
    if settings.APP_ENV == "production":
        tables_exist = await check_tables_exist()
        await db_init(force_drop=False)
        if not tables_exist:
            await create_super_admin()
    else:
        await db_init(force_drop=True)
        await create_super_admin()
        await create_test_user()

    yield

    if settings.APP_ENV == "development":
        await db_drop()
        folder_drop()

    logger.info(f"应用 {app.title} 关闭...")
