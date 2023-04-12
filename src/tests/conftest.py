from collections.abc import Iterator
from os import environ
from typing import cast

from app.config import Settings, get_settings
from app.main import create_application
from beartype import beartype
from fastapi.testclient import TestClient
from pydantic import AnyUrl
from pytest import fixture
from tortoise.contrib.fastapi import register_tortoise


@beartype
def get_settings_override() -> Settings:
    return Settings(
        testing=cast(bool, 1),
        database_url=cast(AnyUrl, environ.get("DATABASE_TEST_URL")),
    )


@fixture(scope="module")
def test_app() -> Iterator[TestClient]:
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@fixture(scope="module")
def test_app_with_db() -> Iterator[TestClient]:
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client
