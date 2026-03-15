from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.domains.news.application.request.save_news_request import SaveNewsRequest
from app.domains.news.application.request.search_news_request import SearchNewsRequest
from app.domains.news.application.response.save_news_response import SaveNewsResponse
from app.domains.news.application.response.search_news_response import SearchNewsResponse
from app.domains.news.application.usecase.save_news_usecase import SaveNewsUseCase
from app.domains.news.application.usecase.search_news_usecase import SearchNewsUseCase
from app.domains.news.di import get_save_news_usecase, get_search_news_usecase

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/search", response_model=SearchNewsResponse)
async def search_news(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    usecase: SearchNewsUseCase = Depends(get_search_news_usecase),
):
    request = SearchNewsRequest(keyword=keyword, page=page, size=size)
    return await usecase.execute(request)


@router.post("/saved", response_model=SaveNewsResponse, status_code=status.HTTP_201_CREATED)
async def save_news(
    request: SaveNewsRequest,
    usecase: SaveNewsUseCase = Depends(get_save_news_usecase),
):
    try:
        return await usecase.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
