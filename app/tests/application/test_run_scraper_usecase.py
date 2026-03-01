import pytest
from app.application.usecases.run_scraper import RunScraperUseCase

@pytest.mark.asyncio
async def test_run_scraper_executes_scraper(fake_scraper):
    usecase = RunScraperUseCase(scraper=fake_scraper)
    result = await usecase.execute("dummy_request")
    assert len(result) == 1
    fake_scraper.scrape.assert_awaited_once()