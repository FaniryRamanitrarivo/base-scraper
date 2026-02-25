import pytest
from app.application.usecases.scrape_jobs import ScrapeJobsUseCase


class FakeScraper:
    async def scrape(self, url):
        return ["job1", "job2"]


@pytest.mark.asyncio
async def test_usecase_calls_scraper():
    scraper = FakeScraper()
    usecase = ScrapeJobsUseCase(scraper)

    result = await usecase.execute("https://test.com")

    assert result == ["job1", "job2"]