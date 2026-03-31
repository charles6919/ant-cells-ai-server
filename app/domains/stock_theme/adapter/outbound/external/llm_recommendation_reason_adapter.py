from app.domains.stock_theme.application.port.recommendation_reason_port import RecommendationReasonPort
from app.domains.stock_theme.domain.service.recommendation_reason_service import RecommendationReasonService
from app.infrastructure.external.llm_client_port import LLMClientPort


class LLMRecommendationReasonAdapter(RecommendationReasonPort):
    def __init__(self, llm_client: LLMClientPort):
        self.llm_client = llm_client

    async def generate_reason(
        self,
        stock_name: str,
        matched_keywords: list[str],
        stock_themes: list[str],
    ) -> str:
        prompt = RecommendationReasonService.build_prompt(
            stock_name=stock_name,
            matched_keywords=matched_keywords,
            stock_themes=stock_themes,
        )
        return await self.llm_client.generate(
            prompt=prompt,
            instructions=RecommendationReasonService.INSTRUCTIONS,
        )
