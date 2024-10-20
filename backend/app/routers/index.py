from fastapi import APIRouter, Response

router = APIRouter(prefix="/index")


@router.get("", name="index", description="Index page")
def index() -> Response:
    return Response(content="index page")
