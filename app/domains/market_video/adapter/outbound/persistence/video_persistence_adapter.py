from datetime import datetime
from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.market_video.application.port.video_repository_port import VideoRepositoryPort
from app.domains.market_video.domain.entity.saved_video import SavedVideo
from app.domains.market_video.infrastructure.mapper.saved_video_mapper import SavedVideoMapper
from app.domains.market_video.infrastructure.orm.saved_video_orm import SavedVideoORM


class VideoPersistenceAdapter(VideoRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert(self, video: SavedVideo) -> SavedVideo:
        result = await self._session.execute(
            select(SavedVideoORM).where(SavedVideoORM.video_id == video.video_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.title = video.title
            existing.channel_name = video.channel_name
            existing.published_at = video.published_at
            existing.view_count = video.view_count
            existing.thumbnail_url = video.thumbnail_url
            existing.video_url = video.video_url
            existing.saved_at = datetime.utcnow()
        else:
            self._session.add(SavedVideoMapper.to_orm(video))

        await self._session.commit()
        return video

    async def find_all(self, page: int, size: int) -> tuple[list[SavedVideo], int]:
        count_result = await self._session.execute(
            select(func.count(SavedVideoORM.video_id))
        )
        total = count_result.scalar_one()

        result = await self._session.execute(
            select(SavedVideoORM)
            .order_by(SavedVideoORM.published_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        orms = result.scalars().all()

        return [SavedVideoMapper.to_entity(orm) for orm in orms], total

    async def find_by_video_id(self, video_id: str) -> Optional[SavedVideo]:
        result = await self._session.execute(
            select(SavedVideoORM).where(SavedVideoORM.video_id == video_id)
        )
        orm = result.scalar_one_or_none()
        return SavedVideoMapper.to_entity(orm) if orm else None

    async def find_all_by_title_keywords(
        self, keywords: list[str], page: int, size: int,
    ) -> tuple[list[SavedVideo], int]:
        keyword_filter = or_(
            SavedVideoORM.title.contains(kw) for kw in keywords
        )

        count_result = await self._session.execute(
            select(func.count(SavedVideoORM.video_id)).where(keyword_filter)
        )
        total = count_result.scalar_one()

        result = await self._session.execute(
            select(SavedVideoORM)
            .where(keyword_filter)
            .order_by(SavedVideoORM.published_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        orms = result.scalars().all()

        return [SavedVideoMapper.to_entity(orm) for orm in orms], total
