from fastapi import FastAPI

from app.api.ping import router
from app.db import init_db
from app.log import UVICORN_LOGGER


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


app = create_application()


@app.on_event("startup")  # type: ignore
async def startup_event() -> None:
    UVICORN_LOGGER.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")  # type: ignore
async def shutdown_event() -> None:
    UVICORN_LOGGER.info("Shutting down...")
