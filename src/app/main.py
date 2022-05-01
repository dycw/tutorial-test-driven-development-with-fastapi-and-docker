from os import getenv

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.api.ping import router


def create_application() -> FastAPI:
    app = FastAPI()
    register_tortoise(
        app,
        db_url=getenv("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
    app.include_router(router)
    return app


app = create_application()
