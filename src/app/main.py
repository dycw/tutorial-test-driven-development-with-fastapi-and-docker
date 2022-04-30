from typing import Any

from fastapi import Depends
from fastapi import FastAPI

from app.config import Settings
from app.config import get_settings


app = FastAPI()


@app.get("/ping")
async def pong(*, settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
