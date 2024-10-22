from fastapi import APIRouter, Response

from app.dependencies.auth import UserDep

router = APIRouter(prefix="/index", tags=["Index"])


@router.get("", name="index", description="Index page")
def index(user: UserDep) -> Response:
    return Response(content=f"index page {user=}")
