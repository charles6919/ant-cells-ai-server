import asyncio

from app.domains.stock_theme.application.port.recommendation_reason_port import RecommendationReasonPort
from app.domains.stock_theme.application.port.stock_theme_repository_port import StockThemeRepositoryPort
from app.domains.stock_theme.application.request.recommend_stocks_request import RecommendStocksRequest
from app.domains.stock_theme.application.response.stock_recommendation_response import (
    StockRecommendationItemResponse,
    StockRecommendationResponse,
)
from app.domains.stock_theme.domain.service.stock_recommendation_service import StockRecommendationService, StockRecommendationResult


class RecommendStocksUseCase:
    def __init__(
        self,
        stock_theme_repository: StockThemeRepositoryPort,
        recommendation_reason: RecommendationReasonPort,
    ):
        self.stock_theme_repository = stock_theme_repository
        self.recommendation_reason = recommendation_reason

    async def execute(self, request: RecommendStocksRequest) -> StockRecommendationResponse:
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
