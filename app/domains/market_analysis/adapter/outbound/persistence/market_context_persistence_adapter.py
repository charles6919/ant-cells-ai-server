import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.market_analysis.application.port.market_context_repository_port import MarketContextRepositoryPort
from app.domains.stock_theme.infrastructure.orm.stock_theme_orm import StockThemeORM


class MarketContextPersistenceAdapter(MarketContextRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_stocks(self) -> list[dict]:
        result = await self.session.execute(select(StockThemeORM))
        return [
            {"name": row.name, "code": row.code, "themes": self._parse_themes(row.themes)}
            for row in result.scalars().all()
        ]

    @staticmethod
    def _parse_themes(themes) -> list:
        if isinstance(themes, list):
            return themes
        if isinstance(themes, str) and themes.strip():
            try:
                return json.loads(themes)
            except json.JSONDecodeError:
                return []
        return []
