import os
import shutil
import pytest
from httpx import AsyncClient
from fastapi import UploadFile
from main import app, UPLOAD_DIR

TEST_IMAGE_PATH = "app/tests/test_image.jpg"


@pytest.fixture(scope="session", autouse=True)
def setup_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    yield
    shutil.rmtree(UPLOAD_DIR)


@pytest.mark.asyncio
async def test_upload(monkeypatch):
    with open(TEST_IMAGE_PATH, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 1024)  # dummy PNG

    # Monkeypatching Celery and DB for isolated testing
    monkeypatch.setattr("main.send_email_notification.delay", lambda *a, **kw: None)
    monkeypatch.setattr("main.SessionLocal", lambda: DummyDBSession())

    with open(TEST_IMAGE_PATH, "rb") as f:
        files = {"file": ("test_image.jpg", f, "image/jpeg")}
        data = {"description": "Test kép"}

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/upload", files=files, data=data)

    assert response.status_code == 303  # redirect after successful upload
    os.remove(TEST_IMAGE_PATH)


# Dummy DB session for testing
class DummyDBSession:
    def query(self, *args, **kwargs):
        return []

    def add(self, obj): pass
    def commit(self): pass
    def refresh(self, obj): pass
    def close(self): pass
