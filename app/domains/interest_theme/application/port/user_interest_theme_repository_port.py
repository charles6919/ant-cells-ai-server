from abc import ABC, abstractmethod


class UserInterestThemeRepositoryPort(ABC):

    @abstractmethod
    async def save_all(self, account_id: str, theme_seqs: list[int]) -> None:
        pass

    @abstractmethod
    async def find_theme_names_by_account_id(self, account_id: str) -> list[str]:
        pass

    @abstractmethod
    async def find_theme_seqs_by_account_id(self, account_id: str) -> list[int]:
        pass

    @abstractmethod
    async def delete_all_by_account_id(self, account_id: str) -> None:
        pass
