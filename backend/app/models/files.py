from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class CompleteUploadRequest(BaseModel):
    resumable_identifier: str
    resumable_filename: str


class FileResponse(BaseModel):
    name: str
    size: int


class ListFilesResponse(BaseModel):
    files: list[FileResponse]
