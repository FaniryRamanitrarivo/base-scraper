class ExtractionEngine:

    @staticmethod
    async def extract(browser, config, base_url=None):

        elements = await browser.query_all(config.selector)

        results = []

        for el in elements:

            if config.attribute == "textContent":

                value = await browser.get_text(el)
            else:
                value = await browser.get_attribute(el, config.attribute)

            results.append(value)

        return results
