from beartype import beartype
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from tortoise.fields import DatetimeField, TextField
from tortoise.models import Model


class TextSummary(Model):
    url = TextField()
    summary = TextField()
    created_at = DatetimeField(auto_now_add=True)

    @beartype
    def __str__(self) -> str:
        return self.url


SummarySchema = pydantic_model_creator(TextSummary)
