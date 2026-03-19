from abc import ABC, abstractmethod


class TempTokenPort(ABC):

    @abstractmethod
    async def save(self, token: str, kakao_access_token: str, ttl_seconds: int) -> None:
        pass
