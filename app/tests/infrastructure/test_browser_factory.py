import pytest
from unittest.mock import patch, AsyncMock
from app.infrastructure.browsers.browser_factory import BrowserFactory
from app.application.dto.product_links_payload import EngineConfig


@pytest.mark.asyncio
async def test_browser_factory_valid():
    engine = EngineConfig(
        browser="playwright",
        headless=True,
    )

    with patch(
        "app.infrastructure.browsers.playwright.playwright_browser.PlaywrightBrowser.create",
        new_callable=AsyncMock
    ) as mock_create:

        mock_create.return_value = AsyncMock()

        factory = BrowserFactory()
        browser = await factory.create(engine)

        assert browser is not None
        mock_create.assert_called_once()


@pytest.mark.asyncio
async def test_browser_factory_invalid():
    class FakeEngine:
        browser = "invalid-browser"
        headless = True
        timeout = 30000

    factory = BrowserFactory()

    with pytest.raises(ValueError):
        await factory.create(FakeEngine())