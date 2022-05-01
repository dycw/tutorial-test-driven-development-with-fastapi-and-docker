from typing import Any, cast

from beartype import beartype

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


@beartype
async def get(*, id: int) -> dict[str, Any] | None:
    if summary := cast(
        dict[str, Any], await TextSummary.filter(id=id).first().values()
    ):
        return summary
    else:
        return None


@beartype
async def get_all() -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], await TextSummary.all().values())


@beartype
async def post(*, payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(url=payload.url, summary="dummy summary")
    await summary.save()
    return summary.id
