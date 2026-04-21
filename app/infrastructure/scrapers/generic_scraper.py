from app.domain.services.pipeline.scraper_pipeline import ScraperPipeline
from app.domain.services.pipeline.context import ScraperContext

from app.domain.services.stages.navigation_stage import NavigationStage
from app.domain.services.stages.pagination_stage import PaginationStage
from app.domain.services.stages.extraction_stage import ExtractionStage
from app.domain.services.stages.dedup_stage import DedupStage


class GenericScraper:

    def __init__(self, browser, logger):

        self.browser = browser
        self.logger = logger

        self.pipeline = ScraperPipeline(
            [
                NavigationStage(),
                ExtractionStage(),
                #DedupStage()
            ]
        )

    async def scrape(self, payload):

        # log start
        await self.logger.info("Starting generic scraper")

        context = ScraperContext(
            browser=self.browser,
            payload=payload,
            logger=self.logger
        )

        results = await self.pipeline.run(context)

        # log end
        await self.logger.info(
            f"Scraping finished. {len(results)} items found."
        )

        return results