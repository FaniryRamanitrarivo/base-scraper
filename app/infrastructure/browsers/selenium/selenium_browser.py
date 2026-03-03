import asyncio
from typing import List, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from app.domain.interfaces.browser import Browser


class SeleniumBrowser(Browser):

    def __init__(self, driver):
        self.driver = driver

    @classmethod
    async def create(
        cls,
        service_name: str = "selenium-chrome",
        headless: bool = True,
        timeout: int = 30000,
    ):
        """
        service_name: 'selenium-chrome' ou 'selenium-firefox'
        headless: active/désactive le mode headless
        timeout: timeout en millisecondes
        """

        def build():
            if "chrome" in service_name:
                options = ChromeOptions()
                if headless:
                    options.add_argument("--headless=new")

            elif "firefox" in service_name:
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")

            else:
                raise ValueError(f"Unsupported service_name: {service_name}")

            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            url = f"http://{service_name}:4444/wd/hub"

            driver = webdriver.Remote(
                command_executor=url,
                options=options,
            )

            driver.set_page_load_timeout(timeout / 1000)

            return driver

        loop = asyncio.get_running_loop()
        driver = await loop.run_in_executor(None, build)
        return cls(driver)

    async def get(self, url: str):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.driver.get, url)

    async def query_all(self, selector: str) -> List[Any]:
        """
        Retourne une liste de WebElement via un sélecteur CSS.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.driver.find_elements(By.CSS_SELECTOR, selector),
        )

    async def get_attribute(self, element, attribute: str):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            lambda: element.get_attribute(attribute),
        )

    async def get_text(self, element):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            lambda: element.text,
        )

    async def current_url(self) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.driver.current_url,
        )

    async def content(self) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.driver.page_source,
        )

    async def close(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.driver.quit)