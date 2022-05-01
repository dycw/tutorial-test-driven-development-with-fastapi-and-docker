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


@beartype
def test_read_summary(test_app_with_db: TestClient) -> None:
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries/", data=dumps(payload))
    summary_id = response.json()["id"]
    response = test_app_with_db.get(f"/summaries/{summary_id}")
    assert response.status_code == status.HTTP_200_OK
    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == payload["url"]
    assert response_dict["summary"]
    assert response_dict["created_at"]


@beartype
def test_read_summary_incorrect_id(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.get("/summaries/-1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Summary not found"


@beartype
def test_read_all_summaries(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.post(
        "/summaries/", data=dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]
    response = test_app_with_db.get("/summaries/")
    assert response.status_code == status.HTTP_200_OK
    response_list = response.json()
    assert sum(r["id"] == summary_id for r in response_list) == 1
