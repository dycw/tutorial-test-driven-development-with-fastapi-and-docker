from collections.abc import Iterator
from os import getenv

from pytest import fixture
from starlette.testclient import TestClient

from app.config import Settings
from app.config import get_settings
from app.main import create_application


def get_settings_override() -> Settings:
    return Settings(
        testing=True, database_url=getenv("DATABASE_TEST_URL")  # type: ignore
    )


@fixture(scope="module")
def test_app() -> Iterator[TestClient]:
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client
