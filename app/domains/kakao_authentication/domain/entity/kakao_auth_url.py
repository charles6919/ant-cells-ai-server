from dataclasses import dataclass


@dataclass
class KakaoAuthUrl:
    url: str
    client_id: str
    redirect_uri: str
    response_type: str
