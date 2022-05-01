from beartype import beartype
from fastapi import status
from fastapi.testclient import TestClient


@beartype
def test_ping(test_app: TestClient) -> None:
    response = test_app.get("/ping")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "environment": "dev",
        "ping": "pong!",
        "testing": True,
    }
