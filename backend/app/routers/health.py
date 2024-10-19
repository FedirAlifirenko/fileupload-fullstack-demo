from http import HTTPStatus

from fastapi import APIRouter, Response

router = APIRouter(prefix="/health")


@router.get("", name="health", description="Health check")
async def health() -> Response:
    return Response(status_code=HTTPStatus.OK, content="OK")
