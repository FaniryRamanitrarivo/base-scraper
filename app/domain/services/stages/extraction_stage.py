from app.domain.services.pipeline.stage import ScraperStage
from app.domain.services.engine.extraction_engine import ExtractionEngine


class ExtractionStage(ScraperStage):

    async def run(self, context):

        payload = context.payload

        results = []

        for page_url in context.page_urls:

            await context.browser.get(page_url)

            products = await ExtractionEngine.extract(
                context.browser,
                payload.product_links,
                base_url=page_url
            )

            results.extend(products)

        context.results = results