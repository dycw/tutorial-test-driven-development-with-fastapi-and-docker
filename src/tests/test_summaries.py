from json import dumps

from beartype import beartype
from fastapi import status
from fastapi.testclient import TestClient


@beartype
def test_create_summary(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.post(
        "/summaries/", data=dumps({"url": "https://foo.bar"})
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["url"] == "https://foo.bar"


@beartype
def test_create_summary_invalid_json(test_app: TestClient) -> None:
    response = test_app.post("/summaries/", data=dumps({}))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
