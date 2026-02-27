from abc import ABC, abstractmethod
from typing import List


class Browser(ABC):

    @abstractmethod
    async def get(self, url: str):
        pass

    @abstractmethod
    async def query_all(self, selector: str) -> List:
        pass

    @abstractmethod
    async def get_attribute(self, element, attribute: str):
        pass

    @abstractmethod
    async def get_text(self, element):
        pass

    @abstractmethod
    async def current_url(self) -> str:
        pass