from functools import lru_cache
from os import getenv

from pydantic import BaseSettings
from pydantic.networks import AnyUrl

from app.log import UVICORN_LOGGER


class Settings(BaseSettings):
    environment: str = getenv("ENVIRONMENT", "dev")
    testing: bool = getenv("TESTING", 0)  # type: ignore
    database_url: AnyUrl = getenv("DATABASE_URL")  # type: ignore


@lru_cache
def get_settings() -> BaseSettings:
    UVICORN_LOGGER.info("Loading config settings from the environment...")
    return Settings()
