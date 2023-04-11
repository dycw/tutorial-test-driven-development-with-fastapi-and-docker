from typing import Any

from beartype import beartype
from fastapi import APIRouter, Depends

from app.config import Settings, get_settings

router = APIRouter()


@beartype
@router.get("/ping")
async def pong(*, settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
