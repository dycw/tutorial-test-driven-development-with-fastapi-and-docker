from beartype import beartype

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


@beartype
async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(url=payload.url, summary="dummy summary")
    await summary.save()
    return summary.id
