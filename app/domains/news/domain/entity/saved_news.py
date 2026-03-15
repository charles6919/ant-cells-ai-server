from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class SavedNews:
    title: str
    link: str
    source: str
    published_at: str
    snippet: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid4()))
    saved_at: datetime = field(default_factory=datetime.utcnow)
