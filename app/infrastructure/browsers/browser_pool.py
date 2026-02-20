from app.infrastructure.browsers.selenium.selenium_browser import SeleniumBrowser
from app.infrastructure.browsers.playwright.playwright_browser import PlaywrightBrowser


class BrowserFactory:

    async def create(self, browser_type: str):

        if browser_type == "selenium":
            return await SeleniumBrowser.create()

        if browser_type == "playwright":
            return await PlaywrightBrowser.create()

        raise ValueError("Unsupported browser")
