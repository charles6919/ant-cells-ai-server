from fastapi import HTTPException, status

from app.domains.account.application.port.account_repository_port import AccountRepositoryPort
from app.domains.account.application.port.user_token_port import UserTokenPort
from app.domains.account.application.port.user_token_read_port import UserTokenReadPort
from app.domains.interest_theme.application.port.user_interest_theme_repository_port import UserInterestThemeRepositoryPort


class DeleteAccountUseCase:

    def __init__(
        self,
        user_token_read: UserTokenReadPort,
        account_repository: AccountRepositoryPort,
        user_token: UserTokenPort,
        user_interest_theme_repository: UserInterestThemeRepositoryPort,
    ):
        self.user_token_read = user_token_read
        self.account_repository = account_repository
        self.user_token = user_token
        self.user_interest_theme_repository = user_interest_theme_repository

    async def execute(self, user_token_value: str) -> None:
        account_id = await self.user_token_read.get_account_id(user_token_value)
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired user token",
            )

        await self.user_interest_theme_repository.delete_all_by_account_id(account_id)
        await self.account_repository.delete_by_id(account_id)
        await self.user_token.delete_user_token(user_token_value)
        await self.user_token.delete_kakao_access_token(account_id)
