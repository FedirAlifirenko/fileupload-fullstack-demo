from http import HTTPStatus

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.main import app as fastapi_app


@pytest.fixture
def app() -> FastAPI:
    return fastapi_app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


def test_index(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "OK"}
