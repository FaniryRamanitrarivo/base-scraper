import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# app/tests/test_api.py
def test_scrape_endpoint():
    payload = {
        "url": "https://example.com",
        "browser": "selenium-chrome"  # ou "selenium-firefox"
    }

    response = client.post("/scrape", json=payload)
    assert response.status_code == 200