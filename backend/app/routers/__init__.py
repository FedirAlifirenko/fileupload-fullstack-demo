from fastapi import APIRouter

from app.routers.files import router as files_router
from app.routers.health import router as health_router
from app.routers.index import router as index_router
from app.routers.notifications import router as notifications_router

__all__ = ["router"]

router = APIRouter(prefix="/api")

router.include_router(health_router)
router.include_router(index_router)
router.include_router(files_router)
router.include_router(notifications_router)
