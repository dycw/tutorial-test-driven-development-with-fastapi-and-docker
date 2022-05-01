from typing import cast

from fastapi import APIRouter
from fastapi import status

from app.api.crud import post
from app.models.pydantic import SummaryPayloadSchema
from app.models.pydantic import SummaryResponseSchema


router = APIRouter()


@router.post(
    "/",
    response_model=SummaryResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_summary(
    payload: SummaryPayloadSchema,
) -> SummaryResponseSchema:
    summary_id = await post(payload)
    return cast(SummaryResponseSchema, {"id": summary_id, "url": payload.url})
