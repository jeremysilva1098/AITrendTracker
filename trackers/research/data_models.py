from pydantic import BaseModel
from typing import List


class Article(BaseModel):
    title: str
    summary: str
    categories: List[str]
    publishDate: str
    link: str


class ArticleSummary(BaseModel):
    title: str
    summary: str
    link: str