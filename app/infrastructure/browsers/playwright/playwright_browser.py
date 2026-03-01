from playwright.async_api import async_playwright
from app.domain.interfaces.browser import Browser


class PlaywrightBrowser(Browser):

    def __init__(self, browser, page):
        self.browser = browser
        self.page = page

    @classmethod
    async def create(cls, headless: bool = True, timeout: int = 30000):
        pw = await async_playwright().start()
        browser = await pw.chromium.launch(headless=headless)
        page = await browser.new_page()
        page.set_default_timeout(timeout)
        return cls(browser, page)

    async def get(self, url: str):
        await self.page.goto(url)

    async def query_all(self, selector: str) -> List:
        # Retourne une liste d'ElementHandle utilisables par get_attribute et get_text
        return await self.page.query_selector_all(selector)

    async def get_attribute(self, element, attribute: str):
        # 'element' ici est un ElementHandle fourni par query_all
        return await element.get_attribute(attribute)

    async def get_text(self, element):
        # 'element' ici est un ElementHandle
        return await element.inner_text()

    async def current_url(self) -> str:
        return self.page.url

    # --- Méthodes utilitaires ---
    async def content(self):
        return await self.page.content()

    async def close(self):
        await self.browser.close()