from typing import Annotated

from fastapi import Depends

from app.services import NotificationsService


_notifications_service = NotificationsService()


def get_notifications_service() -> NotificationsService:
    global _notifications_service
    return _notifications_service


NotificationsServiceDep = Annotated[
    NotificationsService, Depends(get_notifications_service)
]
