from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


@pytest.fixture(scope="session")
def anyio_backend():
    """To solve the ERROR at setup of test_read_root[asyncio]
    Ref: https://stackoverflow.com/a/72996947
    """
    return "asyncio"


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """提供 FastAPI 应用实例的 fixture
    作用范围: 测试会话期间(session级)
    """
    from app.main import app

    return app


@pytest.fixture(scope="session", autouse=True)
async def life() -> AsyncGenerator[None, None]:
    """全局生命周期管理 fixture(自动使用)
    作用范围: 测试会话期间(session级)
    """
    from app.core.lifecycle import (
        create_super_admin,
        create_test_user,
        db_drop,
        db_init,
        folder_drop,
        folder_init,
    )

    folder_init()
    await db_init(force_drop=True)
    await create_super_admin()
    await create_test_user()
    yield
    await db_drop()
    folder_drop()


@pytest.fixture(scope="session")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """提供异步测试客户端的 fixture
    作用范围: 测试会话期间(session级)"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def test_user_token_headers(client: AsyncClient) -> dict[str, str]:
    """普通用户认证头 fixture
    作用范围: 测试会话期间(session级)
    """
    response = await client.post(
        "/api/tokens",
        data={"username": "test_user_0", "password": "123456"},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture(scope="session")
async def test_admin_token_headers(client: AsyncClient) -> dict[str, str]:
    """管理员认证头 fixture
    作用范围: 测试会话期间(session级)
    """
    response = await client.post(
        "/api/tokens",
        data={"username": "test_admin", "password": "123456"},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture(scope="session")
async def test_super_admin_token_headers(client: AsyncClient) -> dict[str, str]:
    """超级管理员认证头 fixture
    作用范围: 测试会话期间(session级)
    """
    response = await client.post(
        "/api/tokens",
        data={"username": "test_super_admin", "password": "123456"},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
