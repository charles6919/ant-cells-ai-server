from urllib.parse import urlencode

from fastapi import HTTPException, status

from app.domains.kakao_authentication.application.port.kakao_oauth_port import KakaoOAuthPort
from app.domains.kakao_authentication.domain.entity.kakao_auth_url import KakaoAuthUrl
from app.infrastructure.config import get_settings

KAKAO_AUTH_BASE_URL = "https://kauth.kakao.com/oauth/authorize"
RESPONSE_TYPE = "code"


class KakaoOAuthAdapter(KakaoOAuthPort):

    def build_auth_url(self) -> KakaoAuthUrl:
        settings = get_settings()

        if not settings.KAKAO_CLIENT_ID:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="KAKAO_CLIENT_ID is not configured",
            )
        if not settings.KAKAO_REDIRECT_URI:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="KAKAO_REDIRECT_URI is not configured",
            )

        params = {
            "client_id": settings.KAKAO_CLIENT_ID,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "response_type": RESPONSE_TYPE,
        }
        url = f"{KAKAO_AUTH_BASE_URL}?{urlencode(params)}"

        return KakaoAuthUrl(
            url=url,
            client_id=settings.KAKAO_CLIENT_ID,
            redirect_uri=settings.KAKAO_REDIRECT_URI,
            response_type=RESPONSE_TYPE,
        )
