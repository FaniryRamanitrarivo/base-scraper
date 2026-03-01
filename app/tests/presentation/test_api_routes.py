import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.presentation.api.scrap.scraper_routes import router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_scrape_product_links_endpoint(client):

    fake_result = [
        {"title": "Product 1", "url": "https://example.com/1"},
        {"title": "Product 2", "url": "https://example.com/2"},
    ]

    payload = {
        "engine": {
            "browser": "playwright",
            "headless": True
        },
        "entry_points": [
            "https://example.com"
        ],
        "product_links": {
            "type": "selector",
            "selector": "a.product-link"
        }
    }

    with patch(
        "app.presentation.api.scrap.scraper_routes.BrowserFactory"
    ) as mock_factory, patch(
        "app.presentation.api.scrap.scraper_routes.RunScraperUseCase"
    ) as mock_usecase:

        mock_factory_instance = mock_factory.return_value
        mock_factory_instance.create = AsyncMock(return_value="fake_browser")

        mock_usecase_instance = mock_usecase.return_value
        mock_usecase_instance.execute = AsyncMock(return_value=fake_result)

        response = client.post("/scrap/product-links", json=payload)

        assert response.status_code == 200
        assert response.json()["total"] == 2
        assert response.json()["data"] == fake_result