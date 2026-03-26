from datetime import datetime

from pydantic import BaseModel


class CreateBoardResponse(BaseModel):
    board_id: str
    title: str
    content: str
    account_id: str
    created_at: datetime
    updated_at: datetime
