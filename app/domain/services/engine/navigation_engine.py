class NavigationEngine:

    @staticmethod
    async def resolve_navigation(context, entry_url, steps, extractor):

        browser = context.browser
        logger = context.logger
        current_urls = [entry_url]

        for step in steps:

            await logger.info(f"[{step.name}] starting extracting : {step.name}")

            next_urls = []
            visited = set()

            for url in current_urls:

                try:

                    await logger.info(f"Entering page : {url}")

                    await browser.get(url)

                    links = await extractor.extract(
                        browser,
                        step.extract_links,
                        base_url=url
                    )

                    await logger.info(f"Start extraction on the page: {url}")

                    for link in links:
                        if link not in visited:
                            visited.add(link)
                            next_urls.append(link)

                except Exception as e:
                    print(f"Navigation error on {url}: {e}")

            current_urls = next_urls
            
            if len(current_urls) > 0:
                await logger.success(f"[{step.name}] : {len(current_urls)} elements found on the page", current_urls)
            else:
                await logger.warning(f"[{step.name}] No elements found on the page")

        return current_urls