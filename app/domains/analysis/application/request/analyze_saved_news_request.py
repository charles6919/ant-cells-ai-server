from pydantic import BaseModel, Field


class AnalyzeSavedNewsRequest(BaseModel):
    news_id: str = Field(..., min_length=1)
