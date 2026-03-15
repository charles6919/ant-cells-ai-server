from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.news.adapter.outbound.external.serp_news_adapter import SerpNewsAdapter
from app.domains.news.adapter.outbound.persistence.saved_news_repository_impl import SavedNewsRepositoryImpl
from app.domains.news.application.request.save_news_request import SaveNewsRequest
from app.domains.news.application.request.search_news_request import SearchNewsRequest
from app.domains.news.application.response.save_news_response import SaveNewsResponse
from app.domains.news.application.response.search_news_response import SearchNewsResponse
from app.domains.news.application.usecase.save_news_usecase import SaveNewsUseCase
from app.domains.news.application.usecase.search_news_usecase import SearchNewsUseCase
from app.infrastructure.config import get_settings
from app.infrastructure.database.database import get_db_session

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/search", response_model=SearchNewsResponse)
async def search_news(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    settings = get_settings()
    adapter = SerpNewsAdapter(api_key=settings.SERP_API_KEY)
    usecase = SearchNewsUseCase(news_search_port=adapter)

    request = SearchNewsRequest(keyword=keyword, page=page, size=size)
    return await usecase.execute(request)


@router.post("/saved", response_model=SaveNewsResponse, status_code=status.HTTP_201_CREATED)
async def save_news(
    request: SaveNewsRequest,
    session: AsyncSession = Depends(get_db_session),
):
    repository = SavedNewsRepositoryImpl(session)
    usecase = SaveNewsUseCase(saved_news_repository=repository)

    try:
        return await usecase.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
