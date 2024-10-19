from fastapi import APIRouter
from starlette.testclient import TestClient
from http import HTTPStatus


def test_index(client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("index")
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.text == "index page"
