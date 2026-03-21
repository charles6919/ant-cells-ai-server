from abc import ABC, abstractmethod
from typing import Optional

from app.domains.authentication.domain.entity.temp_user_info import TempUserInfo


class TempTokenLookupPort(ABC):

    @abstractmethod
    async def get_user_info(self, token: str) -> Optional[TempUserInfo]:
        """Redis에서 temp_token:{token}에 저장된 사용자 정보를 조회한다."""
        pass
