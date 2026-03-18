from dataclasses import dataclass
from typing import Optional


@dataclass
class KakaoAccessToken:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    scope: Optional[str] = None
