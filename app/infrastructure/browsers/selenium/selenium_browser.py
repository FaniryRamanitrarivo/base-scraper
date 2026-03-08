import asyncio
from typing import List, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
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
        Crée une instance de Selenium à distance avec des optimisations extrêmes 
        pour les connexions lentes et environnements Docker.
        """

        def build():
            # --- CONFIGURATION CHROME ---
            if "chrome" in service_name:
                options = ChromeOptions()
                if headless:
                    options.add_argument("--headless=new")
                
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-extensions")
                # options.add_argument("--blink-settings=imagesEnabled=false")
                options.add_argument("--mute-audio")
                options.add_argument("--disable-remote-fonts") # Gain de bande passante
                
                # 'eager' rend la main dès que le DOM est interactif
                options.page_load_strategy = 'eager' 
                options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # --- CONFIGURATION FIREFOX ---
            elif "firefox" in service_name:
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                
                # Optimisations réseau Firefox via les préférences (about:config)
                options.set_preference("permissions.default.image", 2)       # Bloque les images
                options.set_preference("permissions.default.stylesheet", 2)  # Bloque les CSS (optionnel, très rapide)
                options.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false") # Bloque Flash
                options.set_preference("media.autoplay.enabled", False)      # Bloque l'autovideo
                options.set_preference("network.http.pipelining", True)      # Accélère les requêtes
                options.set_preference("network.http.proxy.pipelining", True)
                
                # Bloque le chargement des polices distantes (très lourd sur les sites modernes)
                options.set_preference("browser.display.use_document_fonts", 0)
                
                options.page_load_strategy = 'eager'

            else:
                raise ValueError(f"Unsupported service_name: {service_name}")

            # URL du Grid Selenium dans Docker
            url = f"http://{service_name}:4444/wd/hub"

            try:
                driver = webdriver.Remote(
                    command_executor=url,
                    options=options,
                )
                
                # Conversion millisecondes -> secondes
                driver.set_page_load_timeout(timeout / 1000)
                driver.implicitly_wait(5) 
                
                return driver
            except Exception as e:
                print(f"CRITICAL: Impossible de se connecter au Grid Selenium ({service_name}): {e}")
                raise

        loop = asyncio.get_running_loop()
        driver = await loop.run_in_executor(None, build)
        return cls(driver)

    async def get(self, url: str):
        """
        Navigue vers une URL avec une tolérance aux échecs réseau.
        """
        loop = asyncio.get_running_loop()
        try:
            await loop.run_in_executor(None, self.driver.get, url)
        except TimeoutException:
            # Sur une connexion à 1Mbps, on log mais on ne crash pas forcément l'app
            print(f"⚠️ Navigation Timeout sur {url}. Tentative de continuer avec le DOM partiel...")
        except WebDriverException as e:
            print(f"❌ Navigation Error sur {url}: {e}")

    async def query_all(self, selector: str) -> List[Any]:
        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(
                None,
                lambda: self.driver.find_elements(By.CSS_SELECTOR, selector),
            )
        except Exception as e:
            print(f"Erreur lors du query_all ({selector}): {e}")
            return []

    async def get_attribute(self, element, attribute: str):
        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(
                None,
                lambda: element.get_attribute(attribute),
            )
        except Exception:
            return None

    async def get_text(self, element):
        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(
                None,
                lambda: element.text,
            )
        except Exception:
            return ""

    async def current_url(self) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.driver.current_url,
        )

    async def content(self) -> str:
        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(
                None,
                lambda: self.driver.page_source,
            )
        except Exception:
            return ""

    async def close(self):
        loop = asyncio.get_running_loop()
        try:
            await loop.run_in_executor(None, self.driver.quit)
        except Exception as e:
            print(f"Erreur lors de la fermeture du driver: {e}")