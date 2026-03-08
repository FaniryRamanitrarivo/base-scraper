from urllib.parse import urljoin


class ExtractionEngine:

    @staticmethod
    async def extract(browser, config, base_url=None):
        results = []

        elements = await browser.query_all(config.selector)

        for el in elements:

            if config.attribute == "textContent":
                value = await browser.get_text(el)
            else:
                value = await browser.get_attribute(el, config.attribute)

            if not value:
                continue

            # Normalisation URL
            if base_url and isinstance(value, str):
                value = urljoin(base_url, value)

            results.append(value)

        return results