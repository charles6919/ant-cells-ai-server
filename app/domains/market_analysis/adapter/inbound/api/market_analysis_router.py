from fastapi import APIRouter, Cookie, Depends

from app.domains.market_analysis.application.request.analyze_question_request import AnalyzeQuestionRequest
from app.domains.market_analysis.application.response.analyze_question_response import AnalyzeQuestionResponse
from app.domains.market_analysis.application.usecase.analyze_question_usecase import AnalyzeQuestionUseCase
from app.domains.market_analysis.di import get_analyze_question_usecase

router = APIRouter(prefix="/market-analysis", tags=["market_analysis"])


@router.post("/question", response_model=AnalyzeQuestionResponse)
async def analyze_question(
    request: AnalyzeQuestionRequest,
    user_token: str = Cookie(..., alias="user_token"),
    usecase: AnalyzeQuestionUseCase = Depends(get_analyze_question_usecase),
):
    return await usecase.execute(user_token=user_token, request=request)
