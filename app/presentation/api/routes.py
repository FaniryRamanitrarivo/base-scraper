from fastapi import APIRouter
from app.application.dto.scrape_request import ScrapeRequest
from app.application.usecases.scrape_jobs import ScrapeJobsUseCase
from app.infrastructure.browsers.browser_factory import BrowserFactory
from app.domain.services.scraper_engine import GenericScraper

router = APIRouter()


@router.post("/scrape")
async def scrape(payload: ScrapeRequest):

    factory = BrowserFactory()
    browser = await factory.create(payload.engine)

    scraper = GenericScraper(browser)
    usecase = ScrapeJobsUseCase(scraper)

    return await usecase.execute(payload.url)
