from beartype import beartype
from fastapi import APIRouter, Depends

from app.config import Settings, get_settings

router = APIRouter()


@router.get("/ping")
@beartype
async def pong(*, settings: Settings = Depends(get_settings)) -> dict[str, str | bool]:
    return {
        "ping": "pong4",
        "environment": settings.environment,
        "testing": settings.testing,
    }
