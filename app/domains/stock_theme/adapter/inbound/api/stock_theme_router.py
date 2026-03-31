from typing import Optional

from fastapi import APIRouter, Cookie, Depends

from app.domains.stock_theme.application.request.recommend_stocks_request import RecommendStocksRequest
from app.domains.stock_theme.application.response.stock_recommendation_response import StockRecommendationResponse
from app.domains.stock_theme.application.response.stock_theme_response import StockThemeListResponse
from app.domains.stock_theme.application.usecase.get_stock_themes_usecase import GetStockThemesUseCase
from app.domains.stock_theme.application.usecase.recommend_stocks_usecase import RecommendStocksUseCase
from app.domains.stock_theme.di import get_recommend_stocks_usecase, get_stock_themes_usecase

router = APIRouter(prefix="/stock-themes", tags=["stock_theme"])


@router.get("", response_model=StockThemeListResponse)
async def get_stock_themes(
    theme: Optional[str] = None,
    user_token: str = Cookie(..., alias="user_token"),
    usecase: GetStockThemesUseCase = Depends(get_stock_themes_usecase),
):
    return await usecase.execute(user_token=user_token, theme=theme)


@router.post("/recommend", response_model=StockRecommendationResponse)
async def recommend_stocks(
    request: RecommendStocksRequest,
    user_token: str = Cookie(..., alias="user_token"),
    usecase: RecommendStocksUseCase = Depends(get_recommend_stocks_usecase),
):
    return await usecase.execute(user_token=user_token, request=request)
