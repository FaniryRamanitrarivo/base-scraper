from app.domain.services.pipeline.stage import ScraperStage
from app.domain.services.engine.navigation_engine import NavigationEngine
from app.domain.services.engine.extraction_engine import ExtractionEngine


class NavigationStage(ScraperStage):

    async def run(self, context):

        payload = context.payload
        logger = context.logger

        await logger.info("[NavigationStage] starting extraction navigation")

        if not payload.navigation_flow:
            context.category_urls = context.entry_points

            await logger.warning(
                f"[NavigationStage] no navigation flow. "
                f"{len(context.entry_points)} entry points used as categories"
            )

            return context

        urls = []

        for entry in context.entry_points:

            await logger.info(f"[NavigationStage] Extract navigation from : {entry}")

            links = await NavigationEngine.resolve_navigation(
                context,
                str(entry),
                payload.navigation_flow,
                ExtractionEngine
            )

            urls.extend(links)

        context.category_urls = urls

        await logger.info(
            f"[NavigationStage] finished. {len(urls)} category urls collected"
        )

        return context