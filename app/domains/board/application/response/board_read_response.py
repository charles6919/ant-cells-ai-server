from datetime import datetime

from pydantic import BaseModel


class BoardReadResponse(BaseModel):
    board_id: str
    title: str
    content: str
    nickname: str
    created_at: datetime
    updated_at: datetime
