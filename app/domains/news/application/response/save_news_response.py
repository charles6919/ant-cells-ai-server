from datetime import datetime

from pydantic import BaseModel


class SaveNewsResponse(BaseModel):
    id: str
    saved_at: datetime
