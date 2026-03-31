from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.market_analysis.adapter.outbound.cache.user_token_read_redis_adapter import UserTokenReadRedisAdapter
from app.domains.market_analysis.adapter.outbound.external.langchain_analysis_adapter import LangChainAnalysisAdapter
from app.domains.market_analysis.adapter.outbound.persistence.market_context_persistence_adapter import MarketContextPersistenceAdapter
from app.domains.market_analysis.application.usecase.analyze_question_usecase import AnalyzeQuestionUseCase
from app.infrastructure.cache.redis_client import get_redis_client
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import get_db_session


def get_analyze_question_usecase(
    session: AsyncSession = Depends(get_db_session),
) -> AnalyzeQuestionUseCase:
    settings = get_settings()
    return AnalyzeQuestionUseCase(
        market_context_repository=MarketContextPersistenceAdapter(session=session),
        llm_analysis=LangChainAnalysisAdapter(api_key=settings.OPENAI_API_KEY),
        user_token_read=UserTokenReadRedisAdapter(redis_client=get_redis_client()),
    )
