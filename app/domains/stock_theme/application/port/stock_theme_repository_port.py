from abc import ABC, abstractmethod
from typing import Optional

from app.domains.stock_theme.domain.entity.stock_theme import StockTheme


class StockThemeRepositoryPort(ABC):
    @abstractmethod
    async def find_all(self) -> list[StockTheme]:
        """등록된 모든 방산주 종목을 반환한다."""
        pass

    @abstractmethod
    async def find_by_theme(self, theme: str) -> list[StockTheme]:
        """특정 테마 키워드에 해당하는 종목을 반환한다."""
        pass

    @abstractmethod
    async def exists_any(self) -> bool:
        """등록된 종목이 하나라도 있는지 확인한다."""
        pass

    @abstractmethod
    async def save_all(self, stocks: list[StockTheme]) -> None:
        """종목 목록을 일괄 저장한다."""
        pass
