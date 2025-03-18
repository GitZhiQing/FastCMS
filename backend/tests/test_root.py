import pytest
from httpx import AsyncClient

from app import settings


@pytest.mark.anyio
async def test_read_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "debug": settings.DEBUG,
        "host": settings.HOST,
        "port": settings.PORT,
    }
