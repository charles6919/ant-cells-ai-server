from abc import ABC, abstractmethod
from typing import Optional

from app.domains.session.domain.entity.session_data import SessionData


class SessionStorePort(ABC):

    @abstractmethod
    async def save(self, session: SessionData, ttl_seconds: int) -> None:
        pass

    @abstractmethod
    async def find_by_token(self, token: str) -> Optional[SessionData]:
        pass

    @abstractmethod
    async def delete(self, token: str) -> None:
        pass
