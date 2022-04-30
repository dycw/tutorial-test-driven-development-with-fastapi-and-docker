from os import getenv
from typing import Any

from fastapi import Depends
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings
from app.config import get_settings


app = FastAPI()


register_tortoise(
    app,
    db_url=getenv("DATABASE_URL"),
    modules={"models": ["app.models.tortoise"]},
    generate_schemas=False,
    add_exception_handlers=True,
)


@app.get("/ping")
async def pong(*, settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
