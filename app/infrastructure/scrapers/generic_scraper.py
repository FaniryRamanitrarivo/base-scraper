from app.domain.interfaces.scraper import Scraper
from app.domain.services.extraction_engine import ExtractionEngine
from app.domain.services.navigation_engine import NavigationEngine
from app.domain.services.pagination_engine import PaginationEngine

class GenericScraper(Scraper):

    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger

    async def scrape(self, payload):

        await self.logger.info("Scraping started")

        all_results = []

        for entry in payload.entry_points:

            await self.logger.info("Processing entry point", entry)
            # Step 1: Navigation
            if payload.navigation_flow:
                category_urls = await NavigationEngine.resolve_navigation(
                    self.browser,
                    entry,
                    payload.navigation_flow,
                    ExtractionEngine
                )

                await self.logger.info("Navigation resolved", len(category_urls))
            
            else:
                category_urls = [entry]

            # Step 2: Pagination
            for url in category_urls:

                await self.logger.info("Processing category", url)

                if payload.pagination:
                    urls = PaginationEngine.build_urls(url, payload.pagination)
                else:
                    urls = [url]

            # Step 3: Product extraction
                for page_url in urls:

                    await self.logger.info("Scraping page", page_url)

                    await self.browser.get(page_url)

                    products = await ExtractionEngine.extract(
                        self.browser,
                        payload.product_links,
                        base_url=page_url
                    )

                    await self.logger.info(
                        "Products extracted",
                        {"count": len(products)}
                    )

                    all_results.extend(products)
                    
        await self.logger.info("Scraping finished", {"total": len(all_results)})

        return list(set(all_results))