from abc import ABC, abstractmethod


class UserTokenPort(ABC):

    @abstractmethod
    async def save_user_token(self, user_token: str, account_id: str, ttl_seconds: int) -> None:
        """Redis에 user_token:{user_token} = account_id 로 저장한다."""
        pass

    @abstractmethod
    async def save_kakao_access_token(self, account_id: str, kakao_access_token: str, ttl_seconds: int) -> None:
        """Redis에 kakao_token:{account_id} = kakao_access_token 으로 저장한다."""
        pass

    @abstractmethod
    async def delete_user_token(self, user_token: str) -> None:
        """Redis에서 user_token 세션을 삭제한다."""
        pass

    @abstractmethod
    async def delete_kakao_access_token(self, account_id: str) -> None:
        """Redis에서 kakao_token을 삭제한다."""
        pass
