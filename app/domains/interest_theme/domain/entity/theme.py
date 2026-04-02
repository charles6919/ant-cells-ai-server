from dataclasses import dataclass
from datetime import datetime


@dataclass
class Theme:
    seq: int
    theme: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
