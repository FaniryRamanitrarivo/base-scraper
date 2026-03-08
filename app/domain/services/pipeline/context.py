class ScraperContext:

    def __init__(self, browser, payload, logger):

        self.browser = browser
        self.payload = payload
        self.logger = logger
        self.entry_points = [str(url) for url in payload.entry_points]
        
        self.category_urls = []
        self.page_urls = []
        self.results = []

        self.metrics = {}