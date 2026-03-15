from typing import List

from pydantic import BaseModel


class AnalyzeArticleResponse(BaseModel):
    keywords: List[str]
    sentiment: str
    sentiment_score: float
