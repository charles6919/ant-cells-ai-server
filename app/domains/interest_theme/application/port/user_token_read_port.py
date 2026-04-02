from abc import ABC, abstractmethod
from typing import Optional


class UserTokenReadPort(ABC):
    @abstractmethod
    async def get_account_id(self, user_token: str) -> Optional[str]:
        pass
