from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from app.dependencies.auth import get_current_user_ws
from app.dependencies.notifications import NotificationsServiceDep

router = APIRouter(
    prefix="/notifications",
    dependencies=[Depends(get_current_user_ws)],
    tags=["Notifications"],
)


@router.websocket("/ws", name="notifications-ws")
async def websocket_endpoint(
    websocket: WebSocket,
    service: NotificationsServiceDep,
) -> None:
    await websocket.accept()
    service.add_client(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        service.remove_client(websocket)
