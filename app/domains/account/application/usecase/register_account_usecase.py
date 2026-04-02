import uuid
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status

from app.domains.account.application.port.account_repository_port import AccountRepositoryPort
from app.domains.account.application.port.temp_token_validation_port import TempTokenValidationPort
from app.domains.account.application.port.user_token_port import UserTokenPort
from app.domains.account.domain.entity.account import Account
from app.domains.interest_theme.application.port.user_interest_theme_repository_port import UserInterestThemeRepositoryPort

USER_TOKEN_TTL_SECONDS = 3600  # 1 hour


class RegisterAccountUseCase:

    def __init__(
        self,
        account_repository: AccountRepositoryPort,
        temp_token: TempTokenValidationPort,
        user_token: UserTokenPort,
        user_interest_theme_repository: UserInterestThemeRepositoryPort,
    ):
        self.account_repository = account_repository
        self.temp_token = temp_token
        self.user_token = user_token
        self.user_interest_theme_repository = user_interest_theme_repository

    async def execute(
        self,
        temp_token: str,
        nickname: str,
        email: str,
        interest_theme_seqs: Optional[list[int]] = None,
    ) -> tuple[Account, str]:
        kakao_access_token = await self.temp_token.get(temp_token)
        if kakao_access_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Temp token is expired or invalid",
            )

        account = Account(
            id=str(uuid.uuid4()),
            email=email,
            kakao_id=None,
            nickname=nickname,
            created_at=datetime.utcnow(),
        )
        await self.account_repository.save(account)

        user_token_value = str(uuid.uuid4())

        await self.user_token.save_kakao_access_token(
            account_id=account.id,
            kakao_access_token=kakao_access_token,
            ttl_seconds=USER_TOKEN_TTL_SECONDS,
        )
        await self.user_token.save_user_token(
            user_token=user_token_value,
            account_id=account.id,
            ttl_seconds=USER_TOKEN_TTL_SECONDS,
        )

        await self.temp_token.delete(temp_token)

        if interest_theme_seqs:
            await self.user_interest_theme_repository.save_all(account.id, interest_theme_seqs)

        print(f"[Register] account_id={account.id}, user_token_prefix={user_token_value[:8]}...")

        return account, user_token_value
