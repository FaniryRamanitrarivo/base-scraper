from abc import ABC, abstractmethod


class ScraperStage(ABC):

    @abstractmethod
    async def run(self, context):
        pass