from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.interest_theme.application.port.theme_repository_port import ThemeRepositoryPort
from app.domains.interest_theme.domain.entity.theme import Theme
from app.domains.interest_theme.infrastructure.mapper.theme_mapper import ThemeMapper
from app.domains.interest_theme.infrastructure.orm.theme_orm import ThemeORM


class ThemePersistenceAdapter(ThemeRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all_active(self) -> list[Theme]:
        result = await self.session.execute(
            select(ThemeORM).where(ThemeORM.is_active == True)
        )
        return [ThemeMapper.to_entity(row) for row in result.scalars().all()]

    async def find_active_seqs(self) -> set[int]:
        result = await self.session.execute(
            select(ThemeORM.seq).where(ThemeORM.is_active == True)
        )
        return set(result.scalars().all())
