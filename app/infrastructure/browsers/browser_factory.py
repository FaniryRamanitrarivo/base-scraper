from app.infrastructure.browsers.selenium.selenium_browser import SeleniumBrowser
from app.infrastructure.browsers.playwright.playwright_browser import PlaywrightBrowser
from app.application.dto.product_links_payload import EngineConfig


class BrowserFactory:

    async def create(self, engine: EngineConfig):

        if engine.browser == "selenium-chrome":
            return await SeleniumBrowser.create(
                service_name="selenium-chrome",
                headless=engine.headless,
                timeout=engine.timeout,
            )

        if engine.browser == "selenium-firefox":
            return await SeleniumBrowser.create(
                service_name="selenium-firefox",
                headless=engine.headless,
                timeout=engine.timeout,
            )

        if engine.browser == "playwright":
            return await PlaywrightBrowser.create(
                headless=engine.headless,
                timeout=engine.timeout,
            )

        raise ValueError(f"Unsupported browser: {engine.browser}")