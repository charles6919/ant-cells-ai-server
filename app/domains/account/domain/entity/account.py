from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Account:
    id: str
    email: str
    kakao_id: Optional[int]
    nickname: Optional[str]
    created_at: datetime
