from fastapi import APIRouter
from app.application.dto.product_links_payload import ProductLinksScraperPayload
from app.infrastructure.browsers.browser_factory import BrowserFactory
from app.infrastructure.scrapers.generic_scraper import GenericScraper
from app.application.usecases.scrape_jobs import ScrapeJobsUseCase


router = APIRouter()


@router.post("/scrap/product-links")
async def scrape(payload: ProductLinksScraperPayload):

    factory = BrowserFactory()
    browser = await factory.create(payload.engine.browser)

    scraper = GenericScraper(browser)

    usecase = ScrapeJobsUseCase(scraper)

    # ⚠️ Ton usecase actuel attend probablement une seule URL
    # Or ton nouveau payload contient plusieurs entry_points
    # Donc on adapte :

    results = []

    for url in payload.entry_points:
        result = await usecase.execute(str(url))
        results.append(result)

    return {
        "run_id": payload.run.run_id if payload.run else None,
        "results": results
    }