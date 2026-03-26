from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Board:
    title: str
    content: str
    account_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def update(self, title: str, content: str) -> None:
        self.title = title
        self.content = content
        self.updated_at = datetime.utcnow()
