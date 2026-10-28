from fastapi.testclient import TestClient

from app.main import app


def test_home_serves_portal_page():
    """FND-02: The root URL serves the portal landing page."""
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "<h1>Campus Support Portal</h1>" in response.text