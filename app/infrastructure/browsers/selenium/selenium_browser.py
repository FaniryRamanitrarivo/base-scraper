import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from app.domain.interfaces.browser import Browser

class SeleniumBrowser(Browser):

    def __init__(self, driver):
        self.driver = driver

    @classmethod
    async def create(cls, service_name="selenium-chrome"):
        """
        service_name doit être 'selenium-chrome' ou 'selenium-firefox'.
        """

        def build():
            # Choix des options selon le navigateur
            if "chrome" in service_name:
                options = ChromeOptions()
            elif "firefox" in service_name:
                options = FirefoxOptions()
            else:
                raise ValueError(f"Unsupported service_name: {service_name}")

            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            # URL interne du conteneur Docker
            url = f"http://{service_name}:4444/wd/hub"

            return webdriver.Remote(command_executor=url, options=options)

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