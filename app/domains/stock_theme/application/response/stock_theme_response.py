from pydantic import BaseModel


class StockThemeItemResponse(BaseModel):
    name: str
    code: str
    themes: list[str]


class StockThemeListResponse(BaseModel):
    total: int
    stocks: list[StockThemeItemResponse]
