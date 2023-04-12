from pydantic import AnyUrl, BaseModel


class SummaryPayloadSchema(BaseModel):
    url: AnyUrl


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int  # noqa: A003
