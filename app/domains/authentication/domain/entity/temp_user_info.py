from dataclasses import dataclass
from typing import Optional


@dataclass
class TempUserInfo:
    nickname: Optional[str]
    email: Optional[str]
