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
def test_create_summaries_invalid_json(test_app: TestClient) -> None:
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
    response = test_app.post("/summaries/", data=dumps({"url": "invalid://url"}))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"


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
    response = test_app_with_db.get("/summaries/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Summary not found"
    response = test_app_with_db.get("/summaries/0/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


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


@beartype
def test_remove_summary(test_app_with_db: TestClient) -> None:
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries/", data=dumps(payload))
    summary_id = response.json()["id"]
    response = test_app_with_db.delete(f"/summaries/{summary_id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": summary_id} | payload


@beartype
def test_remove_summary_incorrect_id(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.delete("/summaries/999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Summary not found"


@beartype
def test_update_summary(test_app_with_db: TestClient) -> None:
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries/", data=dumps(payload))
    summary_id = response.json()["id"]
    response = test_app_with_db.put(
        f"/summaries/{summary_id}/",
        data=dumps({"summary": "updated!"} | payload),
    )
    assert response.status_code == status.HTTP_200_OK
    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == payload["url"]
    assert response_dict["summary"] == "updated!"
    assert response_dict["created_at"]


@beartype
def test_update_summary_incorrect_id(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.put(
        "/summaries/999/",
        data=dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Summary not found"


@beartype
def test_update_summary_invalid_json(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.post(
        "/summaries/", data=dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]
    response = test_app_with_db.put(f"/summaries/{summary_id}/", data=dumps({}))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "summary"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


@beartype
def test_update_summary_invalid_keys(test_app_with_db: TestClient) -> None:
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries/", data=dumps(payload))
    summary_id = response.json()["id"]
    response = test_app_with_db.put(f"/summaries/{summary_id}/", data=dumps(payload))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "summary"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
