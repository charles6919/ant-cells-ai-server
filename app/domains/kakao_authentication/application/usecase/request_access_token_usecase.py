from fastapi import HTTPException, status

from app.domains.kakao_authentication.application.port.kakao_token_port import KakaoTokenPort
from app.domains.kakao_authentication.application.port.kakao_user_info_port import KakaoUserInfoPort
from app.domains.kakao_authentication.application.response.kakao_user_info_response import KakaoUserInfoResponse


class RequestAccessTokenUseCase:
    def __init__(self, kakao_token: KakaoTokenPort, kakao_user_info: KakaoUserInfoPort):
        self.kakao_token = kakao_token
        self.kakao_user_info = kakao_user_info

    async def execute(self, code: str) -> KakaoUserInfoResponse:
        if not code or not code.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authorization code is required",
            )

        token = await self.kakao_token.request_access_token(code=code)
        user_info = await self.kakao_user_info.get_user_info(access_token=token.access_token)

        print(f"[Kakao User] nickname={user_info.nickname}, email={user_info.email}")

        return KakaoUserInfoResponse(
            kakao_id=user_info.kakao_id,
            nickname=user_info.nickname,
            email=user_info.email,
        )
