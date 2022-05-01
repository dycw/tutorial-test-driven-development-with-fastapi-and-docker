from logging import getLogger
from os import getenv

from beartype import beartype
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise import run_async
from tortoise.contrib.fastapi import register_tortoise


_LOGGER = getLogger("uvicorn")


TORTOISE_ORM = {
    "connections": {"default": getenv("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        }
    },
}


@beartype
def init_db(app: FastAPI, /) -> None:
    register_tortoise(
        app,
        db_url=getenv("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


@beartype
async def generate_schema() -> None:
    _LOGGER.info("Initializing Tortoise...")
    await Tortoise.init(
        db_url=getenv("DATABASE_URL"), modules={"modles": ["models.tortoise"]}
    )
    _LOGGER.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
