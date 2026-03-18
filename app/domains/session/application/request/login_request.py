from pydantic import BaseModel


class LoginRequest(BaseModel):
    user_id: str
    role: str
    auth_password: str
