from logging import getLogger

from fastapi import FastAPI

from app.api.ping import router
from app.db import init_db


_LOGGER = getLogger("uvicorn")


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


APPLICATION = create_application()


@APPLICATION.on_event("startup")  # type: ignore
async def startup_event() -> None:
    _LOGGER.info("Starting up...")
    init_db(APPLICATION)


@APPLICATION.on_event("shutdown")  # type: ignore
async def shutdown_event() -> None:
    _LOGGER.info("Shutting down...")
