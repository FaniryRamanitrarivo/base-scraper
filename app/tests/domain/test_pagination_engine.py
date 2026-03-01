import pytest
from unittest.mock import Mock
from app.domain.services.pagination_engine import PaginationEngine

def test_pagination_engine_builds_correct_urls():
    # Mock de la config attendue par build_urls
    config = Mock()
    config.start = 1
    config.max_pages = 3
    config.pattern = "&page=<PNum>"
    
    base_url = "https://example.com/jobs"
    
    urls = PaginationEngine.build_urls(base_url, config)
    
    assert len(urls) == 3
    assert urls[0] == "https://example.com/jobs&page=1"
    assert urls[1] == "https://example.com/jobs&page=2"
    assert urls[2] == "https://example.com/jobs&page=3"