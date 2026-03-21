from typing import Optional

from pydantic import BaseModel


class AuthenticationMeResponse(BaseModel):
    is_registered: bool
    nickname: Optional[str]
    email: Optional[str]
