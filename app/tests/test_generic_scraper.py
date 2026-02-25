import pytest
from app.infrastructure.scrapers.generic_scraper import GenericScraper


@pytest.mark.asyncio
async def test_scraper_extracts_links(html_jobs):

    class FakeBrowser:
        async def get(self, url): pass
        async def content(self): return html_jobs
        async def close(self): pass

    scraper = GenericScraper(FakeBrowser())

    jobs = await scraper.scrape("https://example.com")

    assert len(jobs) == 2
    assert jobs[0].title == "Python Dev"
    assert jobs[0].url == "https://example.com/job1"