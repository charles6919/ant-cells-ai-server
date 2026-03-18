from pydantic import BaseModel


class KakaoAuthUrlResponse(BaseModel):
    url: str
    client_id: str
    redirect_uri: str
    response_type: str
