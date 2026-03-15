from abc import ABC, abstractmethod
from typing import Optional

from app.domains.news.domain.entity.saved_news import SavedNews


class SavedNewsRepositoryPort(ABC):
    @abstractmethod
    async def save(self, saved_news: SavedNews) -> SavedNews:
        pass

    @abstractmethod
    async def find_by_link(self, link: str) -> Optional[SavedNews]:
        pass
