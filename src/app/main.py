from typing import Any

from fastapi import FastAPI


app = FastAPI()


@app.get("/ping")
def pong() -> dict[str, Any]:
    return {"ping": "pong!"}
