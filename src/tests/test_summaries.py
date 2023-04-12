from beartype import beartype
from fastapi.testclient import TestClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


@beartype
def test_create_summary(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    assert response.status_code == HTTP_201_CREATED
    assert response.json()["url"] == "https://foo.bar"


@beartype
def test_create_summaries_invalid_json(test_app: TestClient) -> None:
    response = test_app.post("/summaries/", json={})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
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
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == HTTP_200_OK

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


@beartype
def test_read_summary_incorrect_id(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.get("/summaries/999/")
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Summary not found"


@beartype
def test_read_all_summaries(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.post("/summaries/", json={"url": "https://foo.bar"})
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == HTTP_200_OK

    response_list = response.json()
    assert sum(r["id"] == summary_id for r in response_list) == 1
