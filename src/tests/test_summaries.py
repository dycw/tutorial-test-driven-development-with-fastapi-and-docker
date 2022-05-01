from json import dumps

from fastapi import status
from fastapi.testclient import TestClient


def test_create_summary(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.post(
        "/summaries/", data=dumps({"url": "https://foo.bar"})
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["url"] == "https://foo.bar"
