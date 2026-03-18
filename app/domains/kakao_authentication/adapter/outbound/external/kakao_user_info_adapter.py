import httpx
from fastapi import HTTPException, status

from app.domains.kakao_authentication.application.port.kakao_user_info_port import KakaoUserInfoPort
from app.domains.kakao_authentication.domain.entity.kakao_user_info import KakaoUserInfo

KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"


class KakaoUserInfoAdapter(KakaoUserInfoPort):

    async def get_user_info(self, access_token: str) -> KakaoUserInfo:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(KAKAO_USER_INFO_URL, headers=headers)

        if response.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Kakao access token is invalid or expired",
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to retrieve Kakao user info: {response.text}",
            )

        data = response.json()
        kakao_account = data.get("kakao_account", {})
        profile = kakao_account.get("profile", {})

        return KakaoUserInfo(
            kakao_id=data["id"],
            nickname=profile.get("nickname"),
            email=kakao_account.get("email"),
        )
