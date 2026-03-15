from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.news.application.port.saved_news_repository_port import SavedNewsRepositoryPort
from app.domains.news.domain.entity.saved_news import SavedNews
from app.domains.news.infrastructure.mapper.saved_news_mapper import SavedNewsMapper
from app.domains.news.infrastructure.orm.saved_news_orm import SavedNewsORM


class SavedNewsRepositoryImpl(SavedNewsRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, saved_news: SavedNews) -> SavedNews:
        orm = SavedNewsMapper.to_orm(saved_news)
        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        return SavedNewsMapper.to_entity(orm)

    async def find_by_link(self, link: str) -> Optional[SavedNews]:
        result = await self.session.execute(
            select(SavedNewsORM).where(SavedNewsORM.link == link)
        )
        orm = result.scalar_one_or_none()
        if orm is None:
            return None
        return SavedNewsMapper.to_entity(orm)
