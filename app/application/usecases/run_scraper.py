class RunScraperUseCase:

    def __init__(self, scraper):
        self.scraper = scraper

    async def execute(self, payload):
        return await self.scraper.scrape(payload)