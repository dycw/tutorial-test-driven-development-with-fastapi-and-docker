from logging import getLogger

from fastapi import FastAPI

from app.api import ping
from app.api import summaries
from app.db import init_db


_LOGGER = getLogger("uvicorn")


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(ping.router)
    app.include_router(summaries.router, prefix="/summaries", tags=["summaries"])
    return app


APP = create_application()


@APP.on_event("startup")  # type: ignore
async def startup_event() -> None:
    _LOGGER.info("Starting up...")
    init_db(APP)


@APP.on_event("shutdown")  # type: ignore
async def shutdown_event() -> None:
    _LOGGER.info("Shutting down...")
