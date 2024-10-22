import os
from http import HTTPStatus
from pathlib import Path

import aiofiles
from fastapi import (
    Depends,
    UploadFile,
    HTTPException,
    APIRouter,
    Query,
    BackgroundTasks,
)

from app.models.files import (
    CompleteUploadRequest,
    FileResponse,
    ListFilesResponse,
    MessageResponse,
)
from app.dependencies.auth import get_current_user, UserDep
from app.dependencies.notifications import NotificationsServiceDep

UPLOAD_DIR = Path("./uploaded_files/chunks")
COMPLETED_DIR = Path("./uploaded_files/files")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
COMPLETED_DIR.mkdir(exist_ok=True, parents=True)

READ_CHUNK_SIZE = 1024 * 1024  # 1 MB

router = APIRouter(
    prefix="/files", dependencies=[Depends(get_current_user)], tags=["Files"]
)


@router.get("/upload", name="check-chunk", description="Check if a file chunk exists")
async def check_chunk(
    resumable_identifier: str = Query(..., alias="resumableIdentifier"),
    resumable_chunk_number: int = Query(..., alias="resumableChunkNumber"),
    # resumable_chunk_size: int = Query(..., alias="resumableChunkSize"),
    # resumable_total_size: int = Query(..., alias="resumableTotalSize"),
) -> MessageResponse:
    chunk_path = UPLOAD_DIR / f"{resumable_identifier}_part{resumable_chunk_number}"
    if not chunk_path.exists():
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Chunk not found")

    return MessageResponse(message=f"Chunk {resumable_chunk_number} exists")


@router.post("/upload", name="upload-chunk", description="Upload a file chunk")
async def upload_chunk(
    file: UploadFile,
    resumable_identifier: str = Query(..., alias="resumableIdentifier"),
    resumable_chunk_number: int = Query(..., alias="resumableChunkNumber"),
    # resumable_chunk_size: int = Query(..., alias="resumableChunkSize"),
    # resumable_total_size: int = Query(..., alias="resumableTotalSize"),
) -> MessageResponse:
    chunk_path = UPLOAD_DIR / f"{resumable_identifier}_part{resumable_chunk_number}"
    async with aiofiles.open(chunk_path, "wb") as chunk_file:
        while content := await file.read(READ_CHUNK_SIZE):
            await chunk_file.write(content)

    return MessageResponse(message=f"Chunk {resumable_chunk_number} uploaded")


@router.post(
    "/upload/complete", name="complete-upload", description="Complete file upload"
)
async def complete_upload(
    request: CompleteUploadRequest,
    user: UserDep,
    service: NotificationsServiceDep,
    background_tasks: BackgroundTasks,
) -> MessageResponse:
    resumable_filename = request.resumable_filename
    resumable_identifier = request.resumable_identifier

    # Combine the uploaded chunks to reconstruct the complete file
    output_file_path = COMPLETED_DIR / resumable_filename
    async with aiofiles.open(output_file_path, "wb") as output_file:
        part_number = 1
        while True:
            chunk_path = UPLOAD_DIR / f"{resumable_identifier}_part{part_number}"
            if not chunk_path.exists():
                break

            # Write the chunk to the final file
            async with aiofiles.open(chunk_path, "rb") as chunk_file:
                while chunk := await chunk_file.read(READ_CHUNK_SIZE):
                    await output_file.write(chunk)

            # Remove the chunk after it has been added to the final file
            os.remove(chunk_path)
            part_number += 1

    background_tasks.add_task(
        service.notify_clients, f"File {resumable_filename} uploaded by {user}"
    )
    return MessageResponse(message=f"File {resumable_filename} uploaded successfully")


@router.get("", name="list-files", description="List uploaded files")
async def list_files() -> ListFilesResponse:
    files = [
        FileResponse(name=file_path.name, size=file_path.stat().st_size)
        for file_path in COMPLETED_DIR.iterdir()
        if file_path.is_file()
    ]
    return ListFilesResponse(files=files)
