from typing import Any
from app.domain.services.pipeline.stage import ScraperStage
from app.domain.services.engine.extraction_engine import ExtractionEngine
from app.domain.services.engine.pagination_engine import PaginationEngine

class ExtractionStage(ScraperStage):

    async def run(self, context: Any):
        # 1. Correct the reference to the pagination config
        payload = context.payload
        logger = context.logger
        pagination_cfg = getattr(payload, 'pagination', None) 

        await logger.info("[ExtractionStage] starting extraction product links")
        
        results = []
        urls_to_process = list(getattr(context, 'category_urls', []))
        processed_urls = set()
        
        # 2. Track page progress locally
        # We use a counter to ensure we don't exceed max_pages
        pages_scraped_count = 1 
        
        index = 0
        while index < len(urls_to_process):
            page_url = urls_to_process[index]
            index += 1

            if page_url in processed_urls:
                continue
            
            
            try:
                await logger.info(f"Entering page : {page_url}")

                await context.browser.get(page_url)
                processed_urls.add(page_url)
                
                await logger.info(f"Start extraction on the page: {page_url}")

                # Extract links from current page
                products = await ExtractionEngine.extract(
                    context.browser,
                    payload.product_links,
                    base_url=page_url
                )

                if len(products) > 0: 
                    await logger.success(f"Found {len(products)} links on this page.", products)
                    results.extend(products)
                else:
                    await logger.warning(f"No links found on the page : ", page_url)
                    break
                
                # 3. Pagination Logic - Check if we should find the NEXT page
                if pagination_cfg and pages_scraped_count < pagination_cfg.max_pages:
                    await logger.info(f"Paginating: {pages_scraped_count}/{pagination_cfg.max_pages}")
                    
                    # The engine should use the current context/url to find or build the next link
                    next_page_url = await PaginationEngine.paginate(context, page_url)
                    
                    if next_page_url and next_page_url not in processed_urls:
                        await logger.info(f"Added to queue: {next_page_url}")
                        urls_to_process.append(next_page_url)
                        pages_scraped_count += 1 # Increment only when a new page is queued
                else:
                    if pagination_cfg:
                        await logger.info(f"Pagination stopped: reached limit or no config.")

            except Exception as e:
                await logger.error(f"Error on {page_url}: {str(e)}")

        context.results = list(set(results))






