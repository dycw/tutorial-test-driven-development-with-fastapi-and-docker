from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient


def test_ping(test_app: TestClient) -> None:
    response = test_app.get("/ping")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "environment": "dev",
        "ping": "pong!",
        "testing": True,
    }
