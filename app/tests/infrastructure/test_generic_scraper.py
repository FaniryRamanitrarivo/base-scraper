import pytest
from unittest.mock import Mock, AsyncMock
from app.domain.services.scraper_engine import GenericScraper

@pytest.mark.asyncio
async def test_generic_scraper_orchestration(fake_browser, fake_logger):
    # 1. Initialisation
    scraper = GenericScraper(browser=fake_browser, logger=fake_logger)
    
    # 2. Mock du payload (données d'entrée)
    payload = Mock()
    payload.entry_points = ["https://example.com"]
    payload.navigation_flow = None
    payload.pagination = None
    payload.product_links = Mock(selector=".link", attribute="href")
    
    # 3. Exécution (indispensable d'utiliser await !)
    results = await scraper.scrape(payload)
    
    # 4. Vérifications
    assert isinstance(results, list)
    fake_logger.info.assert_called() # Vérifie que le logging fonctionne
    fake_browser.get.assert_called_with("https://example.com")