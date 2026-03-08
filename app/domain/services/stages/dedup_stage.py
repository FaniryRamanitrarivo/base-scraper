from app.domain.services.pipeline.stage import ScraperStage


class DedupStage(ScraperStage):

    async def run(self, context):

        context.results = list(set(context.results))