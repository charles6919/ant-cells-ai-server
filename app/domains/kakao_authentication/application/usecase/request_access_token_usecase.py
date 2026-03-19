import uuid

from fastapi import HTTPException, status

from app.domains.account.application.port.account_repository_port import AccountRepositoryPort
from app.domains.kakao_authentication.application.port.kakao_token_port import KakaoTokenPort
from app.domains.kakao_authentication.application.port.kakao_user_info_port import KakaoUserInfoPort
from app.domains.kakao_authentication.application.port.temp_token_port import TempTokenPort
from app.domains.kakao_authentication.application.response.kakao_user_info_response import KakaoUserInfoResponse
from app.domains.kakao_authentication.domain.value_object.token_type import TokenType

TEMP_TOKEN_TTL_SECONDS = 300  # 5 minutes


class RequestAccessTokenUseCase:
    def __init__(
        self,
        kakao_token: KakaoTokenPort,
        kakao_user_info: KakaoUserInfoPort,
        account_repository: AccountRepositoryPort,
        temp_token: TempTokenPort,
    ):
        self.kakao_token = kakao_token
        self.kakao_user_info = kakao_user_info
        self.account_repository = account_repository
        self.temp_token = temp_token

    async def execute(self, code: str) -> KakaoUserInfoResponse:
        if not code or not code.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authorization code is required",
            )

        token = await self.kakao_token.request_access_token(code=code)
        user_info = await self.kakao_user_info.get_user_info(access_token=token.access_token)

        print(f"[Kakao User] nickname={user_info.nickname}, email={user_info.email}")

        account = None
        if user_info.email:
            account = await self.account_repository.find_by_email(email=user_info.email)

        if account is not None:
            return KakaoUserInfoResponse(
                kakao_id=user_info.kakao_id,
                nickname=user_info.nickname,
                email=user_info.email,
                is_registered=True,
                account_id=account.id,
                token_type=TokenType.SESSION,
            )

        temp_token_value = str(uuid.uuid4())
        await self.temp_token.save(
            token=temp_token_value,
            kakao_access_token=token.access_token,
            ttl_seconds=TEMP_TOKEN_TTL_SECONDS,
        )

        print(f"[Temp Token] issued=True, token_prefix={temp_token_value[:8]}...")

        return KakaoUserInfoResponse(
            kakao_id=user_info.kakao_id,
            nickname=user_info.nickname,
            email=user_info.email,
            is_registered=False,
            token_type=TokenType.TEMP,
            temp_token=temp_token_value,
        )
