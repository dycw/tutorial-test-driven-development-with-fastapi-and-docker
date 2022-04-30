from tortoise.fields import DatetimeField
from tortoise.fields import TextField
from tortoise.models import Model


class TextSummary(Model):
    url = TextField()
    summary = TextField()
    created_at = DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.url
