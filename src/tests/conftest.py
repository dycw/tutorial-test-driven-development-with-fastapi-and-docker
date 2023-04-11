from collections.abc import Iterator
from os import getenv

from beartype import beartype
from fastapi.testclient import TestClient
from pytest import fixture
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings, get_settings
from app.main import create_application


@beartype
def get_settings_override() -> Settings:
    return Settings(
        testing=True, database_url=getenv("DATABASE_TEST_URL")  # type: ignore
    )


@beartype
@fixture(scope="module")
def test_app() -> Iterator[TestClient]:
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@beartype
@fixture(scope="module")
def test_app_with_db() -> Iterator[TestClient]:
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=getenv("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client
