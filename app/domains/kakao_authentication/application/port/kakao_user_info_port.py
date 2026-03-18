from abc import ABC, abstractmethod

from app.domains.kakao_authentication.domain.entity.kakao_user_info import KakaoUserInfo


class KakaoUserInfoPort(ABC):

    @abstractmethod
    async def get_user_info(self, access_token: str) -> KakaoUserInfo:
        pass
