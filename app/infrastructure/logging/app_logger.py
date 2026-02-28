import logging
import datetime
from app.domain.interfaces.logger import AppLogger


class LiveLogger(AppLogger):

    def __init__(self, websocket_manager=None):
        self.websocket_manager = websocket_manager

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        self.logger = logging.getLogger("scraper")

    async def _send(self, level: str, message: str, data=None):

        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "data": data
        }

        # Console log
        getattr(self.logger, level.lower())(f"{message} | {data}")

        # WebSocket broadcast
        if self.websocket_manager:
            await self.websocket_manager.broadcast(log_entry)

    async def info(self, message: str, data=None):
        await self._send("INFO", message, data)

    async def warning(self, message: str, data=None):
        await self._send("WARNING", message, data)

    async def error(self, message: str, data=None):
        await self._send("ERROR", message, data)