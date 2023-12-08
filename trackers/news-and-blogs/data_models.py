from pydantic import BaseModel

class Article(BaseModel):
    title: str
    source: str
    description: str
    url: str
    content: str


class ArticleSummary(BaseModel):
    title: str
    summary: str
    url: str
    source: str