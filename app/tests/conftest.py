import pytest

class FakeBrowser:
    def __init__(self, html):
        self.html = html
        self.opened = False
        self.closed = False

    async def get(self, url):
        self.opened = True

    async def content(self):
        return self.html

    async def close(self):
        self.closed = True


@pytest.fixture
def html_jobs():
    return """
    <html>
      <body>
        <a href="https://example.com/job1">Python Dev</a>
        <a href="https://example.com/job2">Backend Dev</a>
      </body>
    </html>
    """