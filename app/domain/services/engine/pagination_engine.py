class PaginationEngine:

    @staticmethod
    def build_urls(base_url, config):

        urls = []

        for i in range(config.start, config.max_pages + 1):

            page = config.pattern.replace("<PNum>", str(i))
            url = base_url + page

            urls.append(url)

        return urls