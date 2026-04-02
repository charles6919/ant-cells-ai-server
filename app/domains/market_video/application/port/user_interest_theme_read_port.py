from abc import ABC, abstractmethod


class UserInterestThemeReadPort(ABC):

    @abstractmethod
    async def find_theme_names_by_account_id(self, account_id: str) -> list[str]:
        pass
