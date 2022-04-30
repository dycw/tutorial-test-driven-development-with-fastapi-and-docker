from functools import lru_cache
from logging import getLogger
from os import getenv

from pydantic import BaseSettings
from pydantic.networks import AnyUrl


log = getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = getenv("ENVIRONMENT", "dev")
    testing: bool = getenv("TESTING", 0)  # type: ignore
    database_url: AnyUrl = getenv("DATABASE_URL")  # type: ignore


@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
