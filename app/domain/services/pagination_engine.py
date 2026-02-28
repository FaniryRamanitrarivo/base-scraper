class PaginationEngine:

    @staticmethod
    def build_urls(base_url, config):

        urls = []

        for i in range(config.start, config.max_pages + 1):
            url = base_url + config.pattern.replace("<PNum>", str(i))
            urls.append(url)

        return urls