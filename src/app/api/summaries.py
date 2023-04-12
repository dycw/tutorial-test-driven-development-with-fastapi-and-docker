from typing import Any

from beartype import beartype
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.api.crud import get, get_all, post
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=HTTP_201_CREATED)
@beartype
async def create_summary(*, payload: SummaryPayloadSchema) -> dict[str, int | str]:
    summary_id = await post(payload)
    return {"id": summary_id, "url": payload.url}


@router.get("/{id}/", response_model=SummarySchema)
@beartype
async def read_summary(*, id: int) -> dict[str, Any]:  # noqa: A002
    if (summary := await get(id)) is not None:
        return summary
    raise HTTPException(HTTP_404_NOT_FOUND, detail="Summary not found")


@router.get("/", response_model=list[SummarySchema])
async def read_all_summaries() -> list[Any]:
    return await get_all()
