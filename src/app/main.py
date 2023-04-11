from os import environ

from beartype import beartype
from fastapi import Depends, FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings, get_settings

app = FastAPI()


register_tortoise(
    app,
    db_url=environ.get("DATABASE_URL"),
    modules={"models": ["app.models.tortoise"]},
    add_exception_handlers=True,
)


@app.get("/ping")
@beartype
async def pong(*, settings: Settings = Depends(get_settings)) -> dict[str, str | bool]:
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
