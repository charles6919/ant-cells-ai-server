from pydantic import BaseModel


class KeywordItem(BaseModel):
    keyword: str
    count: int


class RecommendStocksRequest(BaseModel):
    keywords: list[KeywordItem]
