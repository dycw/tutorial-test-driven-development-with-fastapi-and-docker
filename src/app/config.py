from functools import lru_cache
from logging import getLogger
from os import getenv

from pydantic import BaseSettings


log = getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = getenv("ENVIRONMENT", "dev")
    testing: bool = getenv("TESTING", "") == "TESTING"


@lru_cache
async def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
