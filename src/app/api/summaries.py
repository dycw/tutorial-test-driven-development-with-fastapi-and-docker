from typing import Any

from beartype import beartype
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import HTTPException
from fastapi import Path
from fastapi import status

from app.api.crud import delete
from app.api.crud import get
from app.api.crud import get_all
from app.api.crud import post
from app.api.crud import put
from app.models.pydantic import SummaryPayloadSchema
from app.models.pydantic import SummaryResponseSchema
from app.models.pydantic import SummaryUpdatePayloadSchema
from app.models.tortoise import SummarySchema
from app.summarizer import generate_summary


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
async def create_summary(
    *, payload: SummaryPayloadSchema, background_tasks: BackgroundTasks
) -> dict[str, Any]:
    summary_id = await post(payload=payload)
    url = payload.url
    background_tasks.add_task(generate_summary, summary_id=summary_id, url=url)
    return {"id": summary_id, "url": url}


@router.get("/{id}/", response_model=SummarySchema)
@beartype
async def read_summary(*, id: int = Path(..., gt=0)) -> dict[str, Any]:
    if (summary := await get(id=id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found"
        )
    return summary


@router.delete("/{id}/", response_model=SummaryResponseSchema)
async def delete_summary(*, id: int = Path(..., gt=0)) -> dict[str, Any]:
    if (summary := await get(id=id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found"
        )
    await delete(id=id)
    return summary


@router.put("/{id}/", response_model=SummarySchema)
async def update_summary(
    *, id: int = Path(..., gt=0), payload: SummaryUpdatePayloadSchema
) -> dict[str, Any]:
    if (summary := await put(id=id, payload=payload)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found"
        )
    return summary
