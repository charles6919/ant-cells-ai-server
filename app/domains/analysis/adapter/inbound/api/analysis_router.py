from fastapi import APIRouter, HTTPException

from app.domains.analysis.adapter.outbound.external.openai_analysis_adapter import OpenAIAnalysisAdapter
from app.domains.analysis.application.request.analyze_article_request import AnalyzeArticleRequest
from app.domains.analysis.application.response.analyze_article_response import AnalyzeArticleResponse
from app.domains.analysis.application.usecase.analyze_article_usecase import AnalyzeArticleUseCase
from app.infrastructure.config import get_settings

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=AnalyzeArticleResponse)
async def analyze_article(request: AnalyzeArticleRequest):
    settings = get_settings()
    adapter = OpenAIAnalysisAdapter(api_key=settings.OPENAI_API_KEY)
    usecase = AnalyzeArticleUseCase(article_analysis_port=adapter)

    try:
        return await usecase.execute(request)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"기사 분석에 실패했습니다: {str(e)}")
