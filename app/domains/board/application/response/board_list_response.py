from datetime import datetime

from pydantic import BaseModel


class BoardItemResponse(BaseModel):
    board_id: str
    title: str
    content: str
    nickname: str
    created_at: datetime
    updated_at: datetime


class BoardListResponse(BaseModel):
    items: list[BoardItemResponse]
    current_page: int
    total_pages: int
    total_count: int
