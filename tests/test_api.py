# Location: /tests/test_api.py

import pytest
import pytest_asyncio
import httpx
import io
from fastapi import status
import time
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base
from src.db.session import get_db
from src.main import app

# Setup deterministic test database fixture with SQLite
test_engine = create_engine("sqlite:///./test_runner.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

pytestmark = pytest.mark.asyncio
BASE_URL = os.getenv("TEST_BASE_URL", "http://test")

@pytest_asyncio.fixture(scope="function")
async def client():
    if os.getenv("TEST_BASE_URL"):
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            yield client
    else:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL) as client:
            yield client


async def test_health_check(client: httpx.AsyncClient):
    response = await client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok", "message": "API is healthy"}


async def test_upload_resume(client: httpx.AsyncClient, mocker):
    """
    Test 2: Verifies file upload, deduplication hashing, and Celery task dispatch.
    """
    mock_parse_task = mocker.patch("src.api.v1.endpoints.resumes.parse_resume_task")

    fake_file_content = f"This is a fake PDF content {time.time()}".encode("utf-8")
    fake_file = io.BytesIO(fake_file_content)
    file_name = f"test_resume_{time.time()}.pdf"

    response = await client.post(
        "/api/v1/resumes/upload",
        files={"file": (file_name, fake_file, "application/pdf")}
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["status"] == "pending"
    assert "id" in response_data
    assert response_data["message"] == "Resume uploaded successfully, queued for processing."

    mock_parse_task.delay.assert_called_once()
    mock_parse_task.delay.assert_called_with(str(response_data["id"]))


async def test_upload_file_too_large(client: httpx.AsyncClient):
    """
    Test 3: Does our 10MB file size limit work?
    """
    fake_large_file_content = b"A" * (11 * 1024 * 1024)
    fake_large_file = io.BytesIO(fake_large_file_content)

    response = await client.post(
        "/api/v1/resumes/upload",
        files={"file": ("large_file.pdf", fake_large_file, "application/pdf")}
    )

    assert response.status_code == status.HTTP_413_CONTENT_TOO_LARGE
    response_data = response.json()
    assert "File size exceeds 10MB limit" in response_data["detail"]


async def test_email_notification_service(client: httpx.AsyncClient):
    """
    Test 4: Verifies the email notifier test endpoint and mock dispatch.
    """
    response = await client.post(
        "/api/v1/resumes/notify/test?recipientEmail=talent@example.com"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    assert data["delivered"] is True
    assert data["recipient"] == "talent@example.com"
