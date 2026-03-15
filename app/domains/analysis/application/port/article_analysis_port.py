from abc import ABC, abstractmethod

from app.domains.analysis.domain.entity.analysis_result import AnalysisResult


class ArticleAnalysisPort(ABC):
    @abstractmethod
    async def analyze(self, content: str) -> AnalysisResult:
        pass
