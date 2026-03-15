from app.domains.analysis.application.port.article_analysis_port import ArticleAnalysisPort
from app.domains.analysis.application.request.analyze_article_request import AnalyzeArticleRequest
from app.domains.analysis.application.response.analyze_article_response import AnalyzeArticleResponse


class AnalyzeArticleUseCase:
    def __init__(self, article_analysis_port: ArticleAnalysisPort):
        self.article_analysis_port = article_analysis_port

    async def execute(self, request: AnalyzeArticleRequest) -> AnalyzeArticleResponse:
        result = await self.article_analysis_port.analyze(content=request.content)

        return AnalyzeArticleResponse(
            keywords=result.keywords,
            sentiment=result.sentiment,
            sentiment_score=result.sentiment_score,
        )
