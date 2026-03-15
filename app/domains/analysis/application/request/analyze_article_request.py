from pydantic import BaseModel, Field


class AnalyzeArticleRequest(BaseModel):
    content: str = Field(..., min_length=1)
