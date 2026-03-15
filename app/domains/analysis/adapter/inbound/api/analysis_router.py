import logging

from fastapi import APIRouter, Depends, HTTPException

from app.domains.analysis.application.request.analyze_article_request import AnalyzeArticleRequest
from app.domains.analysis.application.response.analyze_article_response import AnalyzeArticleResponse
from app.domains.analysis.application.usecase.analyze_article_usecase import AnalyzeArticleUseCase
from app.domains.analysis.application.usecase.analyze_saved_news_usecase import AnalyzeSavedNewsUseCase
from app.domains.analysis.di import get_analyze_article_usecase, get_analyze_saved_news_usecase

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=AnalyzeArticleResponse)
async def analyze_article(
    request: AnalyzeArticleRequest,
    usecase: AnalyzeArticleUseCase = Depends(get_analyze_article_usecase),
):
    try:
        return await usecase.execute(request)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"기사 분석에 실패했습니다: {str(e)}")


@router.post("/saved-news/{news_id}", response_model=AnalyzeArticleResponse)
async def analyze_saved_news(
    news_id: str,
    usecase: AnalyzeSavedNewsUseCase = Depends(get_analyze_saved_news_usecase),
):
    try:
        return await usecase.execute(news_id=news_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("기사 분석 실패 (news_id=%s)", news_id)
        raise HTTPException(status_code=502, detail=f"기사 분석에 실패했습니다: {str(e)}")
