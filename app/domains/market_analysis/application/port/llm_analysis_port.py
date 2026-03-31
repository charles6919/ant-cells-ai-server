from abc import ABC, abstractmethod


class LLMAnalysisPort(ABC):
    @abstractmethod
    async def analyze(self, question: str, context: str) -> str:
        """방산 컨텍스트를 기반으로 사용자 질문에 대한 답변을 생성한다."""
        pass
