from app.domains.analysis.application.port.article_analysis_port import ArticleAnalysisPort
from app.domains.analysis.application.response.analyze_article_response import AnalyzeArticleResponse
from app.domains.news.application.port.saved_news_repository_port import SavedNewsRepositoryPort


class AnalyzeSavedNewsUseCase:
    def __init__(
        self,
        saved_news_repository: SavedNewsRepositoryPort,
        article_analysis_port: ArticleAnalysisPort,
    ):
        self.saved_news_repository = saved_news_repository
        self.article_analysis_port = article_analysis_port

    async def execute(self, news_id: str) -> AnalyzeArticleResponse:
        saved_news = await self.saved_news_repository.find_by_id(news_id)
        if saved_news is None:
            raise ValueError(f"저장된 기사를 찾을 수 없습니다: {news_id}")

        if not saved_news.content or not saved_news.content.strip():
            raise ValueError("기사 본문이 비어 있어 분석할 수 없습니다")

        result = await self.article_analysis_port.analyze(content=saved_news.content)

        return AnalyzeArticleResponse(
            keywords=result.keywords,
            sentiment=result.sentiment,
            sentiment_score=result.sentiment_score,
        )
