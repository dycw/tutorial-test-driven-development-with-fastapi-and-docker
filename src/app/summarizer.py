from beartype import beartype
from newspaper import Article
from nltk import download
from nltk.data import find


@beartype
def generate_summary(url: str) -> str:
    article = Article(url)
    article.download()
    article.parse()
    try:
        find("tokenizers/punkt")
    except LookupError:
        download("punkt")
    finally:
        article.nlp()
    return article.summary
