from playwright.async_api import async_playwright
from app.domain.interfaces.browser import Browser


class PlaywrightBrowser(Browser):

    def __init__(self, browser, page):
        self.browser = browser
        self.page = page

    @classmethod
    async def create(cls):
        pw = await async_playwright().start()
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        return cls(browser, page)

    async def get(self, url):
        await self.page.goto(url)

    async def content(self):
        return await self.page.content()

    async def close(self):
        await self.browser.close()
