from beartype import beartype
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK


@beartype
def test_home(*, test_app: TestClient) -> None:
    response = test_app.get("/")
    assert response.status_code == HTTP_200_OK
