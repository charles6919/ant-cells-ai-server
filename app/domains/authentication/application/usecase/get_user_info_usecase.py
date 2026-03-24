from typing import Optional

from fastapi import HTTPException, status

from app.domains.account.application.port.account_repository_port import AccountRepositoryPort
from app.domains.authentication.application.port.temp_token_lookup_port import TempTokenLookupPort
from app.domains.authentication.application.port.user_session_lookup_port import UserSessionLookupPort
from app.domains.authentication.application.response.authentication_me_response import AuthenticationMeResponse


class GetUserInfoUseCase:

    def __init__(
        self,
        temp_token_lookup: TempTokenLookupPort,
        user_session_lookup: UserSessionLookupPort,
        account_repository: AccountRepositoryPort,
    ):
        self.temp_token_lookup = temp_token_lookup
        self.user_session_lookup = user_session_lookup
        self.account_repository = account_repository

    async def execute(
        self,
        temp_token: Optional[str] = None,
        user_token: Optional[str] = None,
    ) -> AuthenticationMeResponse:
        if user_token:
            return await self._handle_user_token(user_token)

        if temp_token:
            return await self._handle_temp_token(temp_token)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication token provided",
        )

    async def _handle_user_token(self, user_token: str) -> AuthenticationMeResponse:
        account_id = await self.user_session_lookup.get_account_id(user_token)
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User token is expired or invalid",
            )

        account = await self.account_repository.find_by_id(account_id)
        if account is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account not found",
            )

        print(f"[Authentication Me] user_token_prefix={user_token[:8]}..., nickname={account.nickname}, email={account.email}")

        return AuthenticationMeResponse(
            is_registered=True,
            nickname=account.nickname,
            email=account.email,
        )

    async def _handle_temp_token(self, temp_token: str) -> AuthenticationMeResponse:
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
