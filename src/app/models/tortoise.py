from tortoise.contrib.pydantic.creator import pydantic_model_creator
from tortoise.fields import DatetimeField, IntField, TextField
from tortoise.models import Model


class TextSummary(Model):
    id = IntField(pk=True)
    url = TextField()
    summary = TextField()
    created_at = DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.url


SummarySchema = pydantic_model_creator(TextSummary)
