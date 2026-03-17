from app.domains.analysis.application.port.article_content_port import ArticleContentPort
from app.domains.news.application.port.saved_news_repository_port import SavedNewsRepositoryPort
from app.domains.news.application.request.save_news_request import SaveNewsRequest
from app.domains.news.application.response.save_news_response import SaveNewsResponse
from app.domains.news.domain.entity.saved_news import SavedNews


class SaveNewsUseCase:
    def __init__(
        self,
        saved_news_repository: SavedNewsRepositoryPort,
        article_content_port: ArticleContentPort,
    ):
        self.saved_news_repository = saved_news_repository
        self.article_content_port = article_content_port

    async def execute(self, request: SaveNewsRequest) -> SaveNewsResponse:
        # 이미 관심 기사로 저장한 뉴스인지 체크
        existing = await self.saved_news_repository.find_by_link(request.link)
        if existing:
            raise ValueError("이미 저장된 기사입니다.")

        # 실제 기사의 본문을 뽑아냅니다.
        # usecase 내부에서 특정 세부 사항을 호출하여 처리하는 구조
        # 실제로 LLM에게 감정 분석을 시킬 때
        # link 주고 분석해오라고 하면 응답성도 떨어지고 토큰도 많이 사용하게 됨.
        content = await self.article_content_port.fetch_content(request.link)

        saved_news = SavedNews(
            title=request.title,
            link=request.link,
            source=request.source,
            published_at=request.published_at,
            snippet=request.snippet,
            content=content if content and content.strip() else None,
        )

        saved = await self.saved_news_repository.save(saved_news)

        return SaveNewsResponse(
            id=saved.id,
            saved_at=saved.saved_at,
        )
