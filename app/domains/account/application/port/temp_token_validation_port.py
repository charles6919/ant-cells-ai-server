from abc import ABC, abstractmethod
from typing import Optional


class TempTokenValidationPort(ABC):

    @abstractmethod
    async def get(self, token: str) -> Optional[str]:
        """Redis에서 temp_token:{token} 키로 kakao_access_token을 조회한다."""
        pass

    @abstractmethod
    async def delete(self, token: str) -> None:
        """Redis에서 temp_token:{token} 키를 삭제한다."""
        pass
