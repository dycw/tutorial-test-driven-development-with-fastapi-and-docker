from os import getenv

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


TORTOISE_ORM = {
    "connections": {"default": getenv("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        }
    },
}


def init_db(app: FastAPI, /) -> None:
    register_tortoise(
        app,
        db_url=getenv("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
