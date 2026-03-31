from abc import ABC, abstractmethod


class MarketContextRepositoryPort(ABC):
    @abstractmethod
    async def get_all_stocks(self) -> list[dict]:
        """DB에서 전체 방산주 종목(name, code, themes)을 반환한다."""
        pass
