from abc import ABC, abstractmethod

from app.domains.kakao_authentication.domain.entity.kakao_access_token import KakaoAccessToken


class KakaoTokenPort(ABC):

    @abstractmethod
    async def request_access_token(self, code: str) -> KakaoAccessToken:
        pass
