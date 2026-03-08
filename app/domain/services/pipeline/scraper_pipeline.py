class ScraperPipeline:

    def __init__(self, stages):
        self.stages = stages

    async def run(self, context):

        for stage in self.stages:
            await stage.run(context)

        return context.results