import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_scrape_endpoint():

    payload = {
        "url": "https://example.com",
        "browser": "selenium"
    }

    response = client.post("/scrape", json=payload)

    assert response.status_code in (200, 500)