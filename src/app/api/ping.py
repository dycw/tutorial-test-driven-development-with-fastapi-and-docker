from typing import Any

from fastapi import APIRouter
from fastapi import Depends

from app.config import Settings
from app.config import get_settings


router = APIRouter()


@router.get("/ping")
async def pong(*, settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
