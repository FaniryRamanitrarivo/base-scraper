import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from app.domain.interfaces.browser import Browser


class SeleniumBrowser(Browser):

    def __init__(self, driver):
        self.driver = driver

    @classmethod
    async def create(cls):

        def build():
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            return webdriver.Remote(
                command_executor="http://selenium:4444/wd/hub",
                options=options
            )

        loop = asyncio.get_running_loop()
        driver = await loop.run_in_executor(None, build)
        return cls(driver)

    async def get(self, url):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.driver.get, url)

    async def content(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: self.driver.page_source)

    async def close(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.driver.quit)
