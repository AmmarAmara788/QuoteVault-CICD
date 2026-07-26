import pytest
from quotevault.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_create_then_list(client):
    create = client.post("/api/quotes", json={"text": "Hello", "author": "Ada"})
    assert create.status_code == 201
    assert create.get_json()["quote"]["author"] == "Ada"

    listing = client.get("/api/quotes")
    assert listing.status_code == 200
    assert len(listing.get_json()["quotes"]) == 1


def test_validation_error(client):
    res = client.post("/api/quotes", json={"text": ""})
    assert res.status_code == 400
    assert "text is required" in res.get_json()["errors"]


def test_random_empty_returns_404(client):
    res = client.get("/api/quotes/random")
    assert res.status_code == 404


def test_random_returns_a_quote(client):
    client.post("/api/quotes", json={"text": "One"})
    res = client.get("/api/quotes/random")
    assert res.status_code == 200
    assert res.get_json()["quote"]["text"] == "One"
