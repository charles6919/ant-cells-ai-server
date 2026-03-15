from abc import ABC, abstractmethod


class ArticleContentPort(ABC):
    @abstractmethod
    async def fetch_content(self, url: str) -> str:
        pass
