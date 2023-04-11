from functools import lru_cache
from logging import getLogger
from typing import cast

from beartype import beartype
from pydantic import BaseSettings

_LOGGER = getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = cast(bool, 0)


@lru_cache
@beartype
def get_settings() -> Settings:
    _LOGGER.info("Loading config settings from the environment...")
    return Settings()
