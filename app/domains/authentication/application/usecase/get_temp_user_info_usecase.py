from fastapi import HTTPException, status

from app.domains.authentication.application.port.temp_token_lookup_port import TempTokenLookupPort
from app.domains.authentication.application.response.authentication_me_response import AuthenticationMeResponse


class GetTempUserInfoUseCase:

    def __init__(self, temp_token_lookup: TempTokenLookupPort):
        self.temp_token_lookup = temp_token_lookup

    async def execute(self, temp_token: str) -> AuthenticationMeResponse:
        user_info = await self.temp_token_lookup.get_user_info(temp_token)

        if user_info is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Temp token is expired or invalid",
            )

        print(f"[Authentication Me] temp_token_prefix={temp_token[:8]}..., nickname={user_info.nickname}, email={user_info.email}")

        return AuthenticationMeResponse(
            is_registered=False,
            nickname=user_info.nickname,
            email=user_info.email,
        )
