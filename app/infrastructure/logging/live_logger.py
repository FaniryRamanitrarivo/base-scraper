import logging
import datetime
from app.domain.interfaces.logger import AppLogger


# Définir le niveau custom UNE SEULE FOIS (au chargement du module)
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)


# 👉 injecter la méthode dans Logger (monkey patch)
logging.Logger.success = success


class LiveLogger(AppLogger):

    def __init__(self, websocket_manager=None):
        self.websocket_manager = websocket_manager

        self.logger = logging.getLogger("scraper")

        # Évite d'ajouter plusieurs handlers
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(formatter)

            self.logger.addHandler(console_handler)

        self.logger.propagate = False

    async def _send(self, level: str, message: str, data=None):

        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "level": level.upper(),
            "message": message,
            "data": data
        }

        # ✅ Mapping vers les méthodes réelles
        level_mapping = {
            "success": "success",
            "info": "info",
            "warning": "warning",
            "error": "error"
        }

        log_method_name = level_mapping.get(level.lower(), "info")

        # fallback safe
        log_method = getattr(self.logger, log_method_name, self.logger.info)

        log_method(f"{message} | {data}" if data else message)

        # ✅ WebSocket broadcast
        if self.websocket_manager:
            try:
                await self.websocket_manager.broadcast(log_entry)
            except Exception as e:
                self.logger.error(f"WebSocket broadcast failed: {e}")

    async def success(self, message: str, data=None):
        await self._send("success", message, data)

    async def info(self, message: str, data=None):
        await self._send("info", message, data)

    async def warning(self, message: str, data=None):
        await self._send("warning", message, data)

    async def error(self, message: str, data=None):
        await self._send("error", message, data)