from fastapi import HTTPException, status

from app.domains.market_analysis.application.port.llm_analysis_port import LLMAnalysisPort
from app.domains.market_analysis.application.port.market_context_repository_port import MarketContextRepositoryPort
from app.domains.market_analysis.application.port.user_token_read_port import UserTokenReadPort
from app.domains.market_analysis.application.request.analyze_question_request import AnalyzeQuestionRequest
from app.domains.market_analysis.application.response.analyze_question_response import AnalyzeQuestionResponse
from app.domains.market_analysis.domain.service.market_context_builder_service import MarketContextBuilderService


class AnalyzeQuestionUseCase:
    def __init__(
        self,
        market_context_repository: MarketContextRepositoryPort,
        llm_analysis: LLMAnalysisPort,
        user_token_read: UserTokenReadPort,
    ):
        self.market_context_repository = market_context_repository
        self.llm_analysis = llm_analysis
        self.user_token_read = user_token_read

    async def execute(self, user_token: str, request: AnalyzeQuestionRequest) -> AnalyzeQuestionResponse:
        account_id = await self.user_token_read.get_account_id(user_token)
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired user token",
            )

        stocks = await self.market_context_repository.get_all_stocks()
        context = MarketContextBuilderService.build(stocks)
        answer = await self.llm_analysis.analyze(question=request.question, context=context)

        return AnalyzeQuestionResponse(question=request.question, answer=answer)
