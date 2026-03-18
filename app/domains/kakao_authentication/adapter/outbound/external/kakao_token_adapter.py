import httpx
from fastapi import HTTPException, status

from app.domains.kakao_authentication.application.port.kakao_token_port import KakaoTokenPort
from app.domains.kakao_authentication.domain.entity.kakao_access_token import KakaoAccessToken
from app.infrastructure.config import get_settings

KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
GRANT_TYPE = "authorization_code"


class KakaoTokenAdapter(KakaoTokenPort):

    async def request_access_token(self, code: str) -> KakaoAccessToken:
        settings = get_settings()

        payload = {
            "grant_type": GRANT_TYPE,
            "client_id": settings.KAKAO_CLIENT_ID,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "code": code,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                KAKAO_TOKEN_URL,
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to obtain Kakao access token: {response.text}",
            )

        data = response.json()

        if "access_token" not in data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid response from Kakao token API: {data}",
            )

        return KakaoAccessToken(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expires_in=data["expires_in"],
            refresh_token=data["refresh_token"],
            refresh_token_expires_in=data["refresh_token_expires_in"],
            scope=data.get("scope"),
        )
