import logging
from contextlib import suppress

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class Service:

    _instance = None

    def __new__(cls) -> "Service":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._clients: list[WebSocket] = []

    def add_client(self, client: WebSocket) -> None:
        self._clients.append(client)

    def remove_client(self, client: WebSocket) -> None:
        with suppress(ValueError):
            self._clients.remove(client)

    async def notify_clients(self, message: str) -> None:
        logger.info(f"Sending message to {len(self._clients)} clients")
        print(f"Sending message to {len(self._clients)} clients")
        for client in self._clients:
            await client.send_text(message)
