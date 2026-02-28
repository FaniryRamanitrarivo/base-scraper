from abc import ABC, abstractmethod
from typing import Any

class AppLogger(ABC):

    @abstractmethod
    async def info(self, message: str, data: Any = None):
        pass

    @abstractmethod
    async def warning(self, message: str, data: Any = None):
        pass

    @abstractmethod
    async def error(self, message: str, data: Any = None):
        pass