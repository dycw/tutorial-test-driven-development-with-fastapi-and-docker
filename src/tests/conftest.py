from collections.abc import Iterator
from os import environ
from typing import cast

from beartype import beartype
from pydantic import AnyUrl
from pytest import fixture
from starlette.testclient import TestClient

from app import main
from app.config import Settings, get_settings


@beartype
def get_settings_override() -> Settings:
    return Settings(
        testing=cast(bool, 1),
        database_url=cast(AnyUrl, environ.get("DATABASE_TEST_URL")),
    )


@fixture(scope="module")
def test_app() -> Iterator[TestClient]:
    main.app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(main.app) as test_client:
        yield test_client
