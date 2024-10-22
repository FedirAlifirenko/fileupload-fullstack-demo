import base64
import os
from pathlib import Path
from typing import Any, Generator

import pytest
from fastapi import APIRouter
from starlette.testclient import TestClient
from http import HTTPStatus


@pytest.fixture
def uploaded_files_dir(project_root: Path) -> Path:
    return project_root / "uploaded_files"


@pytest.fixture
def chunk(uploaded_files_dir: Path) -> Generator[None, None, None]:
    chunk_file_path = uploaded_files_dir / "chunks" / "123_part1"
    with chunk_file_path.open("w") as f:
        f.write("test")

    yield

    os.remove(chunk_file_path)


def test_check_chunk_ok(client: TestClient, router: APIRouter, chunk: Any) -> None:
    url = router.url_path_for("check-chunk")
    response = client.get(
        url, params={"resumableIdentifier": "123", "resumableChunkNumber": 1}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Chunk 1 exists"}


def test_check_chunk_not_found(client: TestClient, router: APIRouter) -> None:
    url = router.url_path_for("check-chunk")
    response = client.get(
        url, params={"resumableIdentifier": "123", "resumableChunkNumber": 1}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Chunk not found"}


def test_upload_chunk(
    client: TestClient, router: APIRouter, uploaded_files_dir: Path
) -> None:
    url = router.url_path_for("upload-chunk")
    response = client.post(
        url,
        files={"file": ("test.txt", "testUpload " * 100)},
        params={"resumableIdentifier": "1234", "resumableChunkNumber": 1},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Chunk 1 uploaded"}

    os.remove(uploaded_files_dir / "chunks" / "1234_part1")


@pytest.fixture
def chunks(uploaded_files_dir: Path) -> Generator[None, None, None]:
    for chunk_id in range(1, 3):
        chunk_file_path = uploaded_files_dir / "chunks" / f"234_part{chunk_id}"
        with chunk_file_path.open("w") as f:
            f.write(f"test {chunk_id}\n")
    yield

    for chunk_id in range(1, 3):
        chunk_file_path = uploaded_files_dir / "chunks" / f"234_part{chunk_id}"
        assert not chunk_file_path.exists()

    uploaded_file = uploaded_files_dir / "files" / "CompleteTest.txt"
    assert uploaded_file.exists()
    os.remove(uploaded_file)


def test_complete_upload(client: TestClient, router: APIRouter, chunks: Any) -> None:
    url = router.url_path_for("complete-upload")
    response = client.post(
        url,
        json={"resumable_filename": "CompleteTest.txt", "resumable_identifier": "234"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "File CompleteTest.txt uploaded successfully"}
