from pydantic import BaseModel

class NewsArticle(BaseModel):
    title: str
    source: str
    description: str
    url: str
    content: str


class NewsArticleSummary(BaseModel):
    title: str
    summary: str
    url: str
    source: str