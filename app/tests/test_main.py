import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_index_page():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "Feltöltött képek" in response.text


@pytest.mark.asyncio
async def test_test_celery():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/test-celery")
    assert response.status_code == 200
    assert "message" in response.json()
