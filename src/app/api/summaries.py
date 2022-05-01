from typing import Any

from beartype import beartype
from fastapi import APIRouter, HTTPException, status

from app.api.crud import get, get_all, post
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.get("/", response_model=list[SummarySchema])
@beartype
async def read_all_summaries() -> list[dict[str, Any]]:
    return await get_all()


@router.post(
    "/",
    response_model=SummaryResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
@beartype
async def create_summary(*, payload: SummaryPayloadSchema) -> dict[str, Any]:
    summary_id = await post(payload=payload)
    return {"id": summary_id, "url": payload.url}


@router.get("/{id}/", response_model=SummarySchema)
@beartype
async def read_summary(*, id: int) -> dict[str, Any]:
    if (summary := await get(id=id)) is not None:
        return summary
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found"
        )
