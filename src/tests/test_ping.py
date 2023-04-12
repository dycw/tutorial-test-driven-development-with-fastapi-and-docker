from beartype import beartype
from starlette.testclient import TestClient


@beartype
def test_ping(*, test_app: TestClient) -> None:
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "ping": "pong2", "testing": "True"}
