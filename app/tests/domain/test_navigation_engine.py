# app/tests/domain/test_navigation_engine.py
import pytest
from app.domain.services.navigation_engine import NavigationEngine
from unittest.mock import Mock

@pytest.mark.asyncio
async def test_navigation_engine_calls_browser(fake_browser):
    # NE PAS FAIRE : engine = NavigationEngine(fake_browser)
    # FAIRE :
    steps = [] 
    extractor = Mock()
    await NavigationEngine.resolve_navigation(fake_browser, "http://test.com", steps, extractor)
    # ... tes assertions