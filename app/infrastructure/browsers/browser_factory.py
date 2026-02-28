from app.infrastructure.browsers.selenium.selenium_browser import SeleniumBrowser
from app.infrastructure.browsers.playwright.playwright_browser import PlaywrightBrowser


class BrowserFactory:

    async def create(self, browser_type: str):

        if browser_type == "selenium-chrome":
            return await SeleniumBrowser.create(service_name="selenium-chrome")
        if browser_type == "selenium-firefox":
            return await SeleniumBrowser.create(service_name="selenium-firefox")

        if browser_type == "playwright":
            return await PlaywrightBrowser.create()

        raise ValueError(f"Unsupported browser: {browser_type}")
