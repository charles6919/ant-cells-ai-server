from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.stock_theme.adapter.outbound.cache.user_token_read_redis_adapter import UserTokenReadRedisAdapter
from app.domains.stock_theme.adapter.outbound.external.llm_recommendation_reason_adapter import LLMRecommendationReasonAdapter
from app.domains.stock_theme.adapter.outbound.persistence.stock_theme_persistence_adapter import StockThemePersistenceAdapter
from app.domains.stock_theme.application.usecase.get_stock_themes_usecase import GetStockThemesUseCase
from app.domains.stock_theme.application.usecase.recommend_stocks_usecase import RecommendStocksUseCase
from app.infrastructure.cache.redis_client import get_redis_client
from app.infrastructure.database.database import get_db_session
from app.infrastructure.external.openai_llm_client import get_llm_client


def get_stock_themes_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> GetStockThemesUseCase:
    return GetStockThemesUseCase(
        stock_theme_repository=StockThemePersistenceAdapter(session=session),
        user_token_read=UserTokenReadRedisAdapter(redis_client=get_redis_client()),
    )


def get_recommend_stocks_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> RecommendStocksUseCase:
    return RecommendStocksUseCase(
        stock_theme_repository=StockThemePersistenceAdapter(session=session),
        recommendation_reason=LLMRecommendationReasonAdapter(llm_client=get_llm_client()),
        user_token_read=UserTokenReadRedisAdapter(redis_client=get_redis_client()),
    )
