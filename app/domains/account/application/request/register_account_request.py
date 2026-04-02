from typing import Optional

from pydantic import BaseModel


class RegisterAccountRequest(BaseModel):
    nickname: str
    email: str
    interest_theme_seqs: Optional[list[int]] = None
