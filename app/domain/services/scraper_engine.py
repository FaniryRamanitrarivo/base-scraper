from app.domain.interfaces.scraper import Scraper
from app.domain.services.extraction_engine import ExtractionEngine
from app.domain.services.navigation_engine import NavigationEngine
from app.domain.services.pagination_engine import PaginationEngine

class GenericScraper(Scraper):

    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger

    async def scrape(self, payload):
        await self.logger.info("🚀 Scraping mission started...")
        all_results = []

        for entry in payload.entry_points:
            await self.logger.info(f"🌐 Accessing entry point: {entry}")
            
            # --- Step 1: Navigation ---
            if payload.navigation_flow:
                await self.logger.info("🔎 Analyzing navigation structure...")
                category_urls = await NavigationEngine.resolve_navigation(
                    self.browser,
                    entry,
                    payload.navigation_flow,
                    ExtractionEngine
                )
                
                if category_urls:
                    await self.logger.success(f"✅ Navigation successful: {len(category_urls)} category links found.")
                else:
                    await self.logger.warning(f"⚠️ Navigation flow returned no links for: {entry}")
                    category_urls = []
            else:
                await self.logger.info("⏭️ No navigation flow defined. Using entry point as direct target.")
                category_urls = [entry]

            # --- Step 2 & 3: Pagination and Extraction ---
            for url in category_urls:
                await self.logger.info(f"📂 Processing category: {url}")

                if payload.pagination:
                    urls = PaginationEngine.build_urls(url, payload.pagination)
                    await self.logger.info(f"📑 Pagination detected: {len(urls)} pages to crawl.")
                else:
                    urls = [url]
                    await self.logger.info("📄 Single page detected (no pagination).")

                for index, page_url in enumerate(urls, 1):
                    await self.logger.info(f"📄 [{index}/{len(urls)}] Scraping page: {page_url}")

                    try:
                        await self.browser.get(page_url)
                        
                        products = await ExtractionEngine.extract(
                            self.browser,
                            payload.product_links,
                            base_url=page_url
                        )

                        await self.logger.info(
                            f"📦 Extraction successful: {len(products)} products found on this page.",
                            {"count": len(products)}
                        )
                        all_results.extend(products)

                    except Exception as e:
                        await self.logger.error(f"❌ Error during extraction on {page_url}: {str(e)}")
                    
        await self.logger.info(
            "🏁 Scraping mission finished!", 
            {"total_raw": len(all_results), "total_unique": len(set(all_results))}
        )

        return list(set(all_results))