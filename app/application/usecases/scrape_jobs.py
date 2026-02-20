from app.domain.interfaces.scraper import Scraper


class ScrapeJobsUseCase:

    def __init__(self, scraper: Scraper):
        self.scraper = scraper

    async def execute(self, url: str):
        return await self.scraper.scrape(url)
