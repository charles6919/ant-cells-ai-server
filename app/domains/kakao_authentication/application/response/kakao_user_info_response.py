from typing import Optional

from pydantic import BaseModel

from app.domains.kakao_authentication.domain.value_object.token_type import TokenType


class KakaoUserInfoResponse(BaseModel):
    kakao_id: int
    nickname: Optional[str]
    email: Optional[str]
    is_registered: bool
    account_id: Optional[str] = None
    token_type: Optional[TokenType] = None
    temp_token: Optional[str] = None
