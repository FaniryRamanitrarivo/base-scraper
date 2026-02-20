from abc import ABC, abstractmethod

class Browser(ABC):

    @abstractmethod
    async def get(self, url: str):
        ...

    @abstractmethod
    async def content(self) -> str:
        ...

    @abstractmethod
    async def close(self):
        ...
