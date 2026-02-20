from bs4 import BeautifulSoup
from app.domain.interfaces.scraper import Scraper
from app.domain.entities.job import Job


class GenericScraper(Scraper):

    def __init__(self, browser):
        self.browser = browser

    async def scrape(self, url):

        await self.browser.get(url)
        html = await self.browser.content()

        soup = BeautifulSoup(html, "html.parser")

        jobs = []

        for a in soup.select("a"):
            text = a.get_text(strip=True)
            href = a.get("href")

            if text and href:
                jobs.append(Job(title=text, url=href))

        await self.browser.close()
        return jobs
