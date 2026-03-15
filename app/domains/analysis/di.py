from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.analysis.adapter.outbound.external.openai_analysis_adapter import OpenAIAnalysisAdapter
from app.domains.analysis.application.port.article_analysis_port import ArticleAnalysisPort
from app.domains.analysis.application.usecase.analyze_article_usecase import AnalyzeArticleUseCase
from app.domains.analysis.application.usecase.analyze_saved_news_usecase import AnalyzeSavedNewsUseCase
from app.domains.news.adapter.outbound.persistence.saved_news_repository_impl import SavedNewsRepositoryImpl
from app.domains.news.application.port.saved_news_repository_port import SavedNewsRepositoryPort
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import get_db_session


def get_article_analysis_port() -> ArticleAnalysisPort:
    settings = get_settings()
    return OpenAIAnalysisAdapter(api_key=settings.OPENAI_API_KEY)


def get_saved_news_repository(
    session: AsyncSession = Depends(get_db_session),
) -> SavedNewsRepositoryPort:
    return SavedNewsRepositoryImpl(session=session)


def get_analyze_article_usecase(
    article_analysis_port: ArticleAnalysisPort = Depends(get_article_analysis_port),
) -> AnalyzeArticleUseCase:
    return AnalyzeArticleUseCase(article_analysis_port=article_analysis_port)


def get_analyze_saved_news_usecase(
    saved_news_repository: SavedNewsRepositoryPort = Depends(get_saved_news_repository),
    article_analysis_port: ArticleAnalysisPort = Depends(get_article_analysis_port),
) -> AnalyzeSavedNewsUseCase:
    return AnalyzeSavedNewsUseCase(
        saved_news_repository=saved_news_repository,
        article_analysis_port=article_analysis_port,
    )
