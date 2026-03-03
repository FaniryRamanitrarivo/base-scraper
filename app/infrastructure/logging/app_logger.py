import logging
import datetime
from app.domain.interfaces.logger import AppLogger


class LiveLogger(AppLogger):

    def __init__(self, websocket_manager=None):
        self.websocket_manager = websocket_manager

        self.logger = logging.getLogger("scraper")

        # Évite d'ajouter plusieurs handlers si déjà configuré
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(formatter)

            self.logger.addHandler(console_handler)

        # Empêche double log si root logger configuré ailleurs
        self.logger.propagate = False

    async def _send(self, level: str, message: str, data=None):

        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "data": data
        }

        # ✅ Console log
        log_method = getattr(self.logger, level.lower())
        log_method(f"{message} | {data}" if data else message)

        # ✅ WebSocket broadcast (sécurisé)
        if self.websocket_manager:
            try:
                await self.websocket_manager.broadcast(log_entry)
            except Exception as e:
                self.logger.error(f"WebSocket broadcast failed: {e}")

    async def info(self, message: str, data=None):
        await self._send("info", message, data)

    async def warning(self, message: str, data=None):
        await self._send("warning", message, data)

    async def error(self, message: str, data=None):
        await self._send("error", message, data)