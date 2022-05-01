from typing import Any

from beartype import beartype

from app.models.pydantic import SummaryPayloadSchema
from app.models.pydantic import SummaryUpdatePayloadSchema
from app.models.tortoise import TextSummary


@beartype
async def get(*, id: int) -> dict[str, Any] | None:
    result = await TextSummary.filter(id=id).first().values()
    if isinstance(result, dict) or result is None:
        return result
    else:
        raise TypeError(f"Invaild type: {result}")


@beartype
async def get_all() -> list[dict[str, Any]]:
    if isinstance(result := await TextSummary.all().values(), list):
        return result
    else:
        raise TypeError(f"Invaild type: {result}")


@beartype
async def post(*, payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(url=payload.url, summary="dummy summary")
    await summary.save()
    return summary.id


@beartype
async def delete(*, id: int) -> None:
    if (first := await TextSummary.filter(id=id).first()) is not None:
        await first.delete()


@beartype
async def put(*, id: int, payload: SummaryUpdatePayloadSchema) -> dict[str, Any] | None:
    summaries = TextSummary.filter(id=id)
    if (await summaries.update(url=payload.url, summary=payload.summary)) is None:
        return None
    if (first := summaries.first()) is not None:
        if isinstance(fvalues := await first.values(), dict) or (fvalues is None):
            return fvalues
        else:
            raise TypeError(f"Invaild type: {fvalues}")
    else:
        return None
