from beartype import beartype
from fastapi import Depends, FastAPI

from app.config import Settings, get_settings

app = FastAPI()


@app.get("/ping")
@beartype
async def pong(*, settings: Settings = Depends(get_settings)) -> dict[str, str | bool]:
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
