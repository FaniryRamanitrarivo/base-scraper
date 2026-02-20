from abc import ABC, abstractmethod

class Scraper(ABC):

    @abstractmethod
    async def scrape(self, url: str):
        ...
