import pytest
from unittest.mock import Mock
from app.domain.services.extraction_engine import ExtractionEngine

@pytest.mark.asyncio
async def test_extraction_engine_returns_jobs(fake_browser):
    # On crée un mock pour la config attendue par le moteur
    config = Mock()
    config.selector = ".job"
    config.attribute = "textContent"
    
    # On configure les retours du fake_browser (qui est un AsyncMock via conftest)
    fake_browser.query_all.return_value = ["element1"]
    fake_browser.get_text.return_value = "Dev"

    # Appel de la méthode statique
    results = await ExtractionEngine.extract(fake_browser, config)
    
    assert results == ["Dev"]
    fake_browser.query_all.assert_called_once_with(".job")