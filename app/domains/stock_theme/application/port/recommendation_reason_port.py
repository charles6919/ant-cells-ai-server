from abc import ABC, abstractmethod


class RecommendationReasonPort(ABC):
    @abstractmethod
    async def generate_reason(
        self,
        stock_name: str,
        matched_keywords: list[str],
        stock_themes: list[str],
    ) -> str:
        """매칭된 키워드와 테마를 기반으로 추천 이유 문장을 생성한다."""
        pass
