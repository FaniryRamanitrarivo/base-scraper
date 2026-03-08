from fastapi import APIRouter, WebSocket
from app.application.dto.product_links_payload import ProductLinksScraperPayload
from app.infrastructure.browsers.browser_factory import BrowserFactory
from app.domain.services.scraper_engine import GenericScraper
from app.application.usecases.run_scraper import RunScraperUseCase
from app.infrastructure.logging.websocket_manager import WebSocketManager
from app.infrastructure.logging.live_logger import LiveLogger

router = APIRouter()
ws_manager = WebSocketManager()

@router.post('/scrap/product-links')
async def scrape(payload: ProductLinksScraperPayload):
    
    factory = BrowserFactory()
    browser = await factory.create(
        payload.engine
    )

    logger = LiveLogger(ws_manager)

    scraper = GenericScraper(browser, logger)
    usecase = RunScraperUseCase(scraper)

    result = await usecase.execute(payload)

    return {"total": len(result), "data": result}

@router.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        ws_manager.disconnect(websocket)