from datetime import datetime

from pydantic import BaseModel


class UpdateBoardResponse(BaseModel):
    board_id: str
    title: str
    content: str
    nickname: str
    created_at: datetime
    updated_at: datetime
