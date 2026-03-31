from pydantic import BaseModel


class StockRecommendationItemResponse(BaseModel):
    name: str
    code: str
    themes: list[str]
    matched_keywords: list[str]
    relevance_score: int
    reason: str


class StockRecommendationResponse(BaseModel):
    total: int
    recommendations: list[StockRecommendationItemResponse]
