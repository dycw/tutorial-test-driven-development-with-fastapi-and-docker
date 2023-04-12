from typing import Any, cast

from beartype import beartype

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


@beartype
async def post(payload: SummaryPayloadSchema, /) -> int:
    summary = TextSummary(url=payload.url, summary="dummy summary")
    await summary.save()
    return cast(Any, summary).id


@beartype
async def get(id: int, /) -> dict[str, Any] | None:  # noqa: A002
    if summary := await TextSummary.filter(id=id).first().values():
        return summary
    return None


@beartype
async def get_all() -> list[dict[str, Any]]:
    return await TextSummary.all().values()
