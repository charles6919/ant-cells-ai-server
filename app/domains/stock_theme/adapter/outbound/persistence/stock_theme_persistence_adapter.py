from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.stock_theme.application.port.stock_theme_repository_port import StockThemeRepositoryPort
from app.domains.stock_theme.domain.entity.stock_theme import StockTheme
from app.domains.stock_theme.infrastructure.mapper.stock_theme_mapper import StockThemeMapper
from app.domains.stock_theme.infrastructure.orm.stock_theme_orm import StockThemeORM


class StockThemePersistenceAdapter(StockThemeRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self) -> list[StockTheme]:
        result = await self.session.execute(select(StockThemeORM))
        return [StockThemeMapper.to_entity(row) for row in result.scalars().all()]

    async def find_by_theme(self, theme: str) -> list[StockTheme]:
        result = await self.session.execute(select(StockThemeORM))
        all_stocks = [StockThemeMapper.to_entity(row) for row in result.scalars().all()]
        return [s for s in all_stocks if theme in s.themes]

    async def exists_any(self) -> bool:
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count()).select_from(StockThemeORM)
        )
        return (result.scalar() or 0) > 0

    async def save_all(self, stocks: list[StockTheme]) -> None:
        for stock in stocks:
            self.session.add(StockThemeMapper.to_orm(stock))
        await self.session.commit()
