from abc import ABC, abstractmethod

from app.domains.kakao_authentication.domain.entity.kakao_auth_url import KakaoAuthUrl


class KakaoOAuthPort(ABC):

    @abstractmethod
    def build_auth_url(self) -> KakaoAuthUrl:
        pass
