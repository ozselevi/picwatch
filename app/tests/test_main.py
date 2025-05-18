import os
import shutil
import pytest
from httpx import AsyncClient
from main import app

UPLOAD_DIR = "app/static/uploads"


@pytest.fixture(autouse=True)
def clear_uploads():
    # Minden teszt előtt üríti a feltöltési könyvtárat
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR)

@pytest.mark.asyncio
async def test_index_page_loads():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert "Feltöltés" in response.text

@pytest.mark.asyncio
async def test_image_upload():
    test_file_path = "tests/test_image.jpg"
    with open(test_file_path, "wb") as f:
        f.write(b"test image content")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open(test_file_path, "rb") as f:
            response = await ac.post(
                "/upload",
                data={"description": "Teszt leírás"},
                files={"file": ("test_image.jpg", f, "image/jpeg")}
            )
    assert response.status_code == 303
    assert os.path.exists(os.path.join(UPLOAD_DIR, "test_image.jpg"))

    os.remove(test_file_path)

@pytest.mark.asyncio
async def test_subscribe():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/subscribe", data={"email": "teszt@example.com"})
    assert response.status_code == 303
