class NavigationEngine:

    @staticmethod
    async def resolve_navigation(browser, entry_url, steps, extractor):

        current_urls = [entry_url]

        for step in steps:

            next_urls = []

            for url in current_urls:
                await browser.get(url)

                links = await extractor.extract(
                    browser,
                    step.extract_links,
                    base_url=url
                )

                next_urls.extend(links)

            current_urls = next_urls

        return current_urls