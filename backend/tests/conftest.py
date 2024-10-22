from base64 import b64encode
from pathlib import Path

import pytest
from fastapi import FastAPI, APIRouter
from starlette.testclient import TestClient

from app.main import app as api_app
from app.routers import router as api_router


@pytest.fixture
def app() -> FastAPI:
    return api_app


@pytest.fixture
def router() -> APIRouter:
    return api_router


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture(autouse=True)
def authorize_user(client: TestClient) -> None:
    client.headers.update(
        {"Authorization": f"Basic {b64encode(b'test:test').decode()}"}
    )
