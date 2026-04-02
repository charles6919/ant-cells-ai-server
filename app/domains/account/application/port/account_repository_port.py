from abc import ABC, abstractmethod
from typing import Optional

from app.domains.account.domain.entity.account import Account


class AccountRepositoryPort(ABC):

    @abstractmethod
    async def find_by_id(self, account_id: str) -> Optional[Account]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Account]:
        pass

    @abstractmethod
    async def save(self, account: Account) -> None:
        pass

    @abstractmethod
    async def delete_by_id(self, account_id: str) -> None:
        pass
