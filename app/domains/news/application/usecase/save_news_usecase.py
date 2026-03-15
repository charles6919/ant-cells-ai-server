from app.domains.news.application.port.saved_news_repository_port import SavedNewsRepositoryPort
from app.domains.news.application.request.save_news_request import SaveNewsRequest
from app.domains.news.application.response.save_news_response import SaveNewsResponse
from app.domains.news.domain.entity.saved_news import SavedNews


class SaveNewsUseCase:
    def __init__(self, saved_news_repository: SavedNewsRepositoryPort):
        self.saved_news_repository = saved_news_repository

    async def execute(self, request: SaveNewsRequest) -> SaveNewsResponse:
        existing = await self.saved_news_repository.find_by_link(request.link)
        if existing:
            raise ValueError("이미 저장된 기사입니다.")

        saved_news = SavedNews(
            title=request.title,
            link=request.link,
            source=request.source,
            published_at=request.published_at,
            snippet=request.snippet,
        )

        saved = await self.saved_news_repository.save(saved_news)

        return SaveNewsResponse(
            id=saved.id,
            saved_at=saved.saved_at,
        )
