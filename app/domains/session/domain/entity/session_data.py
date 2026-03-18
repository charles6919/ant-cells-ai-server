from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SessionData:
    token: str
    user_id: str
    role: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=datetime.utcnow)
