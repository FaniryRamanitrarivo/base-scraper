import pytest
from unittest.mock import AsyncMock, Mock
from typing import cast
from fastapi.testclient import TestClient
from app.main import app # Assure-toi que l'import pointe vers ton instance FastAPI

from app.domain.entities.job import Job
from app.domain.interfaces.browser import Browser
from app.domain.interfaces.scraper import Scraper

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_job() -> Job:
    return Job(
        title="Senior Python Developer",
        company="ACME Corp",
        location="Remote",
        url="https://example.com/job/1"
    )

@pytest.fixture
def fake_browser() -> Browser:
    browser = Mock(spec=Browser)
    # On mocke les méthodes asynchrones avec AsyncMock
    browser.get = AsyncMock(return_value=None)
    browser.query_all = AsyncMock(return_value=[])
    browser.get_text = AsyncMock(return_value="text")
    browser.get_attribute = AsyncMock(return_value="attr")
    browser.close = AsyncMock(return_value=None)
    return cast(Browser, browser)

@pytest.fixture
def fake_logger():
    logger = Mock()
    # Dans GenericScraper, tu fais "await self.logger.info", donc AsyncMock
    logger.info = AsyncMock()
    logger.warning = AsyncMock()
    logger.error = AsyncMock()
    logger.debug = AsyncMock()
    return logger

@pytest.fixture
def fake_scraper(sample_job) -> Scraper:
    scraper = Mock(spec=Scraper)
    # scrape est awaité, donc AsyncMock
    scraper.scrape = AsyncMock(return_value=[sample_job])
    return cast(Scraper, scraper)