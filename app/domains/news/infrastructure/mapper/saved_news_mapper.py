from app.domains.news.domain.entity.saved_news import SavedNews
from app.domains.news.infrastructure.orm.saved_news_orm import SavedNewsORM


class SavedNewsMapper:
    @staticmethod
    def to_entity(orm: SavedNewsORM) -> SavedNews:
        return SavedNews(
            id=orm.id,
            title=orm.title,
            link=orm.link,
            source=orm.source,
            published_at=orm.published_at,
            snippet=orm.snippet,
            saved_at=orm.saved_at,
        )

    @staticmethod
    def to_orm(entity: SavedNews) -> SavedNewsORM:
        return SavedNewsORM(
            id=entity.id,
            title=entity.title,
            link=entity.link,
            source=entity.source,
            published_at=entity.published_at,
            snippet=entity.snippet,
            saved_at=entity.saved_at,
        )
