from abc import ABC, abstractmethod
from typing import Optional


class UserTokenReadPort(ABC):
    @abstractmethod
    async def get_account_id(self, user_token: str) -> Optional[str]:
        """Redis에서 session:{user_token} 키로 account_id를 조회한다."""
        pass
