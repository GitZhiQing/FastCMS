import asyncio

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_login_for_access_token(client: AsyncClient):
    """测试获取访问令牌"""
    # 错误的用户名、邮箱或密码
    response = await client.post(
        "/api/tokens",
        data={"username": "test_user_1", "password": "wrong_password"},
    )
    assert response.status_code == 401

    # 正确的邮箱和密码
    response = await client.post(
        "/api/tokens",
        data={"username": "test_user_1@seek2.team", "password": "123456"},
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

    # 正确的用户名和密码
    response = await client.post(
        "/api/tokens",
        data={"username": "test_user_1", "password": "123456"},
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

    await asyncio.sleep(1)  # 休眠 1 s，确保新 token 产生变化
    # 通过 refresh_token 刷新 access_token
    refresh_token = response.cookies["refresh_token"]
    client.cookies.set("refresh_token", refresh_token)
    response = await client.put("/api/tokens")
    assert response.status_code == 200
    new_token = response.json()
    assert "access_token" in new_token
    assert new_token["token_type"] == "bearer"
    assert new_token["access_token"] != token["access_token"]
