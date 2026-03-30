import asyncio

from fastapi import HTTPException, status

from app.domains.stock_theme.application.port.recommendation_reason_port import RecommendationReasonPort
from app.domains.stock_theme.application.port.stock_theme_repository_port import StockThemeRepositoryPort
from app.domains.stock_theme.application.port.user_token_read_port import UserTokenReadPort
from app.domains.stock_theme.application.request.recommend_stocks_request import RecommendStocksRequest
from app.domains.stock_theme.application.response.stock_recommendation_response import (
    StockRecommendationItemResponse,
    StockRecommendationResponse,
)
from app.domains.stock_theme.domain.service.stock_recommendation_service import StockRecommendationService


class RecommendStocksUseCase:
    def __init__(
        self,
        stock_theme_repository: StockThemeRepositoryPort,
        recommendation_reason: RecommendationReasonPort,
        user_token_read: UserTokenReadPort,
    ):
        self.stock_theme_repository = stock_theme_repository
        self.recommendation_reason = recommendation_reason
        self.user_token_read = user_token_read

    async def execute(self, user_token: str, request: RecommendStocksRequest) -> StockRecommendationResponse:
        account_id = await self.user_token_read.get_account_id(user_token)
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired user token",
            )

        keyword_counts = {item.keyword: item.count for item in request.keywords}

        stocks = await self.stock_theme_repository.find_all()
        results = StockRecommendationService.recommend(stocks, keyword_counts)

        reasons = await asyncio.gather(*[
            self.recommendation_reason.generate_reason(
                stock_name=r.stock.name,
                matched_keywords=r.matched_keywords,
                stock_themes=r.stock.themes,
            )
            for r in results
        ])

        return StockRecommendationResponse(
            total=len(results),
            recommendations=[
                StockRecommendationItemResponse(
                    name=r.stock.name,
                    code=r.stock.code,
                    themes=r.stock.themes,
                    matched_keywords=r.matched_keywords,
                    relevance_score=r.relevance_score,
                    reason=reason,
                )
                for r, reason in zip(results, reasons)
            ],
        )
