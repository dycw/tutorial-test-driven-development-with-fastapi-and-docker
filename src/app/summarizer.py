from beartype import beartype
from newspaper import Article
from nltk import download
from nltk.data import find

from app.models.tortoise import TextSummary


@beartype
async def generate_summary(*, summary_id: int, url: str) -> None:
    article = Article(url)
    article.download()
    article.parse()
    try:
        find("tokenizers/punkt")
    except LookupError:
        download("punkt")
    finally:
        article.nlp()
    _ = await TextSummary.filter(id=summary_id).update(summary=article.summary)
