from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.analysis.adapter.outbound.external.web_scraper_adapter import WebScraperAdapter
from app.domains.analysis.application.port.article_content_port import ArticleContentPort
from app.domains.news.adapter.outbound.external.serp_news_adapter import SerpNewsAdapter
from app.domains.news.adapter.outbound.persistence.saved_news_repository_impl import SavedNewsRepositoryImpl
from app.domains.news.application.port.news_search_port import NewsSearchPort
from app.domains.news.application.port.saved_news_repository_port import SavedNewsRepositoryPort
from app.domains.news.application.usecase.save_news_usecase import SaveNewsUseCase
from app.domains.news.application.usecase.search_news_usecase import SearchNewsUseCase
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import get_db_session


def get_news_search_port() -> NewsSearchPort:
    settings = get_settings()
    return SerpNewsAdapter(api_key=settings.SERP_API_KEY)


def get_saved_news_repository(
    session: AsyncSession = Depends(get_db_session),
) -> SavedNewsRepositoryPort:
    return SavedNewsRepositoryImpl(session=session)


def get_article_content_port() -> ArticleContentPort:
    return WebScraperAdapter()


def get_search_news_usecase(
    news_search_port: NewsSearchPort = Depends(get_news_search_port),
) -> SearchNewsUseCase:
    return SearchNewsUseCase(news_search_port=news_search_port)


def get_save_news_usecase(
    saved_news_repository: SavedNewsRepositoryPort = Depends(get_saved_news_repository),
    article_content_port: ArticleContentPort = Depends(get_article_content_port),
) -> SaveNewsUseCase:
    return SaveNewsUseCase(
        saved_news_repository=saved_news_repository,
        article_content_port=article_content_port,
    )
