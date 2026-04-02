from abc import ABC, abstractmethod

from app.domains.interest_theme.domain.entity.theme import Theme


class ThemeRepositoryPort(ABC):

    @abstractmethod
    async def find_all_active(self) -> list[Theme]:
        pass

    @abstractmethod
    async def find_active_seqs(self) -> set[int]:
        pass
